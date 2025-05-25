interface Employee {
    username: string;
    store_id: number;
    phone_number: string;
    user_id: number;
    nearest_dates: Record<string, "Выходной" | "Работаю">;
}

export default Employee