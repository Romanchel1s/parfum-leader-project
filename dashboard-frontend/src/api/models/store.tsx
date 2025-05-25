interface Store {
    id: number;
    name: string;
    lat: string;
    lon: string;
    city: string;
    line1: string;
    line2: string;
    code: string;
    timezone: {
        timezone_type: number;
        timezone: string;
    };
    workTimeStart: string;
    chat: string;
}

export default Store;