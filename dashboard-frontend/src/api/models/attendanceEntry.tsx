interface AttendanceEntry {
    date: string;
    employees: {
      user_id: number;
      was_present: boolean;
    }[];
}

export default AttendanceEntry;