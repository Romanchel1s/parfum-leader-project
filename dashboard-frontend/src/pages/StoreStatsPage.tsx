import React, { useEffect, useState } from 'react';
import api from '../api/apiClient';
import { Autocomplete, Button, CircularProgress, Paper, Stack, Table, TableBody, TableCell, TableHead, TableRow, TextField, Typography } from '@mui/material';
import Store from '../api/models/store';
import dayjs, { Dayjs } from 'dayjs';
import { DateTimePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import AttendanceEntry from '../api/models/attendanceEntry';



type StoreEmployee = {
    user_id: number;
    username: string;
    store_id: number;
    phone_number: string;
    nearest_dates: Record<string, string>;
  };

const StoreStatsPage: React.FC = () => {
    const [data, setData] = useState([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedStoreFilter, setSelectedStoreFilter] = useState<Store | null>(null);
    const [startTime, setStartTime] = useState<Dayjs | null>(dayjs().startOf("month"));
    const [endTime, setEndTime] = useState<Dayjs | null>(dayjs().endOf("month"));
    const [attendanceData, setAttendanceData] = useState<AttendanceEntry[]>([]);
    const [selectedEmployeeId, setSelectedEmployeeId] = useState<number | null>(null);
    const [employees, setEmployees] = useState<StoreEmployee[]>([]);
    

    useEffect(() => {
        const fetchData = async () => {
            try {
                const stores = await api.getAllStores();
                setData(stores);
            } catch (err: unknown) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError("An unknown error occurred");
                }
            } finally {
                setLoading(false);
            }
        };
        fetchData();
      }, []);

    const fetchEmployees = async (storeId: number) => {
    try {
        const result = await api.getStoreEmployees(storeId.toString());
        const simplified = result.map((emp: StoreEmployee) => ({
        user_id: emp.user_id,
        username: emp.username
        }));
        setEmployees(simplified);
    } catch (err) {
        console.error('Failed to load store employees', err);
    }
    };
    
    const getStoreStat = async () => {
        if (!startTime || !endTime || !selectedStoreFilter) return;
        try {
            await fetchEmployees(selectedStoreFilter.id);
            const result: AttendanceEntry[] = await api.getStoreAttendanceStats(
            selectedStoreFilter.id.toString(),
            startTime.format('YYYY-MM-DDTHH:mm:ss'),
            endTime.format('YYYY-MM-DDTHH:mm:ss')
            );
            setAttendanceData(result);
            setSelectedEmployeeId(null); // сбрасываем выбранного сотрудника
        } catch (err) {
            console.error('Failed to get stores attendance', err);
        }
    };


    const renderEmployeeTable = (userId: number) => {
    const rows = attendanceData.map(entry => {
        const emp = entry.employees.find(e => e.user_id === userId);
        return (
        <TableRow key={entry.date}>
            <TableCell>{entry.date}</TableCell>
            <TableCell>{emp?.was_present ? '✅' : '❌'}</TableCell>
        </TableRow>
        );
    });

    return (
        <Paper sx={{ mt: 3 }}>
        <Table>
            <TableHead>
            <TableRow>
                <TableCell>Дата</TableCell>
                <TableCell>Присутствие</TableCell>
            </TableRow>
            </TableHead>
            <TableBody>{rows}</TableBody>
        </Table>
        </Paper>
    );
    };
      
    if (loading) return <CircularProgress />;
    if (error) return <div>Error: {error}</div>;
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Stack spacing={3} sx={{ width: "80%", margin: "auto", marginTop: 4 }}>
                <Typography variant="h5">Выберите временной интервал</Typography>
                <DateTimePicker label="Начало" value={startTime} onChange={setStartTime} />
                <DateTimePicker label="Конец" value={endTime} onChange={setEndTime} />
                <Autocomplete
                    options={data}
                    getOptionLabel={(option: Store) => option.name}
                    renderInput={(params) => <TextField {...params} label="Выберите магазин" />}
                    value={selectedStoreFilter}
                    onChange={(_e, value) => setSelectedStoreFilter(value)}
                    isOptionEqualToValue={(option, value) => option.id === value.id}
                />
                <Button variant="contained" onClick={getStoreStat}>Получить данные</Button>

                {employees.length > 0 && (
                <Autocomplete
                    options={employees}
                    getOptionLabel={(emp) => emp.username}
                    renderInput={(params) => (
                    <TextField {...params} label="Фильтр по сотруднику" />
                    )}
                    value={employees.find(e => e.user_id === selectedEmployeeId) || null}
                    onChange={(_e, value) => setSelectedEmployeeId(value ? value.user_id : null)}
                    isOptionEqualToValue={(option, value) => option.user_id === value.user_id}
                />
                )}
                
                {selectedEmployeeId !== null && renderEmployeeTable(selectedEmployeeId)}
            </Stack>
        </LocalizationProvider>
        
    );
};

export default StoreStatsPage;