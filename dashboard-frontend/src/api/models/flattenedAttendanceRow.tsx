interface FlattenedAttendanceRow {
    id: string;
    date: string;
    store_id: number;
    store_name: string;
    present: number;
    absent: number;
}

export default FlattenedAttendanceRow;