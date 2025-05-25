import { Stack, Typography } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Brush } from 'recharts';

// Тип для записи посещения
interface AttendanceRecord {
    date: string;        // Дата записи в формате "YYYY-MM-DD"
    time: string;        // Время посещения
    was_present: boolean; // Присутствие (true) или отсутствие (false)
}

// Преобразование массива данных посещений в данные для графика
const transformAttendanceData = (attendanceData: AttendanceRecord[]) => {
    // Группируем данные по датам и подсчитываем присутствия и отсутствия
    const groupedData = attendanceData.reduce((acc: Record<string, { present: number; absent: number }>, record) => {
        if (!acc[record.date]) {
            acc[record.date] = { present: 0, absent: 0 };
        }
        if (record.was_present) {
            acc[record.date].present += 1;
        } else {
            acc[record.date].absent += 1;
        }
        return acc;
    }, {});

    // Преобразуем в массив для отображения на графике
    return Object.keys(groupedData).map(date => ({
        date,
        presentCount: groupedData[date].present,
        absentCount: groupedData[date].absent
    }));
};

interface WorkScheduleProps {
    attendanceData: AttendanceRecord[]; // Массив данных о посещениях
}

const WorkSchedule = ({ attendanceData }: WorkScheduleProps) => {
    const chartData = transformAttendanceData(attendanceData);

    return (
        <Stack sx={{ alignItems: 'center', gap: '20px' }}>
            <Typography variant='h5'>График присутствий и отсутствий</Typography>
            <BarChart
                width={800}
                height={500}
                data={chartData}
                margin={{ bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="presentCount" fill="#4caf50" name="Присутствие" />
                <Bar dataKey="absentCount" fill="#f44336" name="Отсутствие" />
                <Brush dataKey="date" height={30} stroke="#8884d8" startIndex={0} endIndex={5} />
            </BarChart>
        </Stack>
    );
};

export default WorkSchedule;
