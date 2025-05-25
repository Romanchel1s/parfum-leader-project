/* eslint-disable react-hooks/exhaustive-deps */
import { Autocomplete, Button, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import {  useEffect, useState } from "react";
import api from "../api/apiClient";
import Store from "../api/models/store";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import dayjs, { Dayjs } from "dayjs";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import AttendanceStatsByDate from "../api/models/attendanceStatsByDate";
import FlattenedAttendanceRow from "../api/models/flattenedAttendanceRow";
import { useNavigate } from "react-router-dom";

const EmployeeManagerPage: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [startTime, setStartTime] = useState<Dayjs | null>(dayjs().startOf("month"));
    const [endTime, setEndTime] = useState<Dayjs | null>(dayjs().endOf("month"));
    const [attendanceStats, setAttendanceStats] = useState<AttendanceStatsByDate[]>([]);
    const [filteredStats, setFilteredStats] = useState<FlattenedAttendanceRow[]>([]);
    const [selectedStoreFilter, setSelectedStoreFilter] = useState<Store | null>(null);


    const storeIdToNameMap = new Map<number, string>(
      data.map((store: Store) => [store.id, store.name])
    );


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

    useEffect(() => {
      const flattened = attendanceStats.flatMap(entry =>
        entry.stores.map((store) => ({
          id: `${entry.date}-${store.store_id}`,
          date: entry.date,
          store_id: store.store_id,
          store_name: storeIdToNameMap.get(store.store_id) || `ID ${store.store_id}`,
          present: store.present,
          absent: store.absent,
        }))
      );
      const filtered = flattened.filter((row) => {
        return (
          !selectedStoreFilter || row.store_id === selectedStoreFilter.id
        );
      });
    
      setFilteredStats(filtered);
    }, [attendanceStats, selectedStoreFilter]);


    const handleGetStoresAttendance = async () => {
      if (!startTime || !endTime) return;
      try {
        const result = await api.getStoresAttendance(startTime.format("YYYY-MM-DDTHH:mm:ss"), endTime.format("YYYY-MM-DDTHH:mm:ss"));
        console.log("Stores Attendance:", result);
        setAttendanceStats(result);
        // Здесь можно сохранить результат в состояние или показать его на странице
      } catch (err) {
        console.error("Failed to get stores attendance", err);
      }
    };
  

    if (loading) return <CircularProgress />;
    if (error) return <div>Error: {error}</div>;
    return (
       <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Stack spacing={3} sx={{ width: "80%", margin: "auto", marginTop: 4 }}>
            <Typography variant="h5">Выберите временной интервал</Typography>
            <DateTimePicker label="Начало" value={startTime} onChange={setStartTime} />
            <DateTimePicker label="Конец" value={endTime} onChange={setEndTime} />
            <Stack direction="row" spacing={2}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleGetStoresAttendance}
                sx={{ flex: 2 }}
              >
                Получить статистику посещаемости магазинов
              </Button>
              <Button
                variant="contained"
                color="secondary"
                onClick={() => navigate("/store-management")}
                sx={{ flex: 1 }}
              >
                Посмотреть статистику конкретного магазина
              </Button>
            </Stack>
            

            <Autocomplete
              options={data}
              getOptionLabel={(option: Store) => option.name}
              renderInput={(params) => <TextField {...params} label="Фильтр по магазину" />}
              value={selectedStoreFilter}
              onChange={(_e, value) => setSelectedStoreFilter(value)}
              isOptionEqualToValue={(option, value) => option.id === value.id}
            />

            <DataGrid
              rows={filteredStats}
              columns={[
                { field: 'date', headerName: 'Дата', flex: 1 },
                { field: 'store_name', headerName: 'Название магазина', flex: 2 },
                { field: 'present', headerName: 'Присутствующих', flex: 1 },
                { field: 'absent', headerName: 'Отсутствующих', flex: 1 },
              ] as GridColDef[]}
              autoHeight
              disableRowSelectionOnClick
              sx={{ mt: 2 }}
            />
          </Stack>
        </LocalizationProvider>
    );
};

export default EmployeeManagerPage;