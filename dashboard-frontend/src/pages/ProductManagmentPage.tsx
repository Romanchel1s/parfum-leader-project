import { useState, useEffect } from "react";
import { TextField, Autocomplete, Button, CircularProgress, Stack, Typography } from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs, { Dayjs } from "dayjs";
import api from "../api/apiClient";
import Product from "../api/models/product";
import ProductInfo from "../api/models/productInfo";
import Store from "../api/models/store";
import StoreSettingsModal from "../components/UpdateCheckModal";

const fetchProductName = async (id: string): Promise<ProductInfo> => {
    try {
        const response = await api.getProduct(id);
        return {
            id: response.id,
            name: response.name,
            beautifulName: response.beautifulName,
            URL: response.URL
        };
    } catch {
        return { id, name: "Неизвестный товар", beautifulName: "Неизвестный товар", URL: "" };
    }
};

const ProductManagementPage = () => {
    const [data, setData] = useState([]);
    const [selectedStore, setSelectedStore] = useState<Store | null>(null);
    const [startTime, setStartTime] = useState<Dayjs | null>(dayjs().startOf("month"));
    const [productNames, setProductNames] = useState<Record<string, ProductInfo>>({});
    const [endTime, setEndTime] = useState<Dayjs | null>(dayjs().endOf("month"));
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [settingsModalOpen, setSettingsModalOpen] = useState(false);

    useEffect(() => {
        const fetchNames = async () => {
            const namesArray = await Promise.all(
                products.map(async (product: Product) => {
                    return fetchProductName(product.prod_id);
                })
            );

            // Преобразуем массив в объект { "id1": { name, beautifulName, URL }, "id2": { ... } }
            const namesObject = namesArray.reduce((acc, product) => {
                acc[product.id] = product;
                return acc;
            }, {} as Record<string, ProductInfo>);

            setProductNames(namesObject);
        };

        if (products.length > 0) {
            fetchNames();
        }
    }, [products]);

    useEffect(() => {
        const fetchStores = async () => {
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
        fetchStores();
    }, []);

    console.log(selectedStore);

    const fetchProducts = async () => {
        if (!startTime || !endTime) return;
        setLoading(true);
        try {
            const response = await api.getProductsByTime(
                selectedStore?.id.toString() || "",
                startTime.format("YYYY-MM-DDTHH:mm:ss"),
                endTime.format("YYYY-MM-DDTHH:mm:ss")
            );
            setProducts(response);
            setError(null);
        } catch (err: unknown) {
            if (err instanceof Error) {
                setError("Товары не найдены");
            } else {
                setError("An unknown error occurred");
            }
        } finally {
            setLoading(false);
        }
    };

    const downloadCSV = () => {
        const csvContent = [
            "prod_id,prod_avail,prod_check_time,prod_store_id,prod_employee_id",
            ...products.map(p => `${p.prod_id},${p.prod_avail},${p.prod_check_time},${p.prod_store_id},${p.prod_employee_id}`)
        ].join("\n");
        
        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "products_report.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    const stats = products.reduce((acc, product) => {
        acc[product.prod_avail ? "available" : "not_available"]++;
        return acc;
    }, { available: 0, not_available: 0 });

    const columns: GridColDef[] = [
        { field: "prod_id", headerName: "ID", flex: 1 },
        { 
            field: "URL", 
            headerName: "Ссылка", 
            flex: 2, 
            renderCell: (params) => {
                const product = productNames[params.row.prod_id];
                return product?.URL ? (
                    <a href={product.URL} target="_blank" rel="noopener noreferrer">
                        {product.name}
                    </a>
                ) : "Нет ссылки";
            }
        },
        { field: "prod_check_time", headerName: "Дата проверки", flex: 1 },
        { field: "prod_avail", headerName: "Наличие", flex: 1 },
        { field: "prod_store_id", headerName: "ID магазина", flex: 1 },
        { field: "prod_employee_id", headerName: "ID сотрудника", flex: 1 },
    ];

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Stack spacing={3} sx={{ width: "80%", margin: "auto", marginTop: 4 }}>
                <Autocomplete
                    options={data}
                    getOptionLabel={(option: Store) => option.name}
                    renderInput={(params) => <TextField {...params} label="Выберите магазин" />}
                    onChange={(_, value) => setSelectedStore(value)}
                    value={selectedStore}
                />
                {selectedStore? <>
                    <Typography variant="h5">Выберите временной интервал</Typography>
                    <DateTimePicker label="Начало" value={startTime} onChange={setStartTime} />
                    <DateTimePicker label="Конец" value={endTime} onChange={setEndTime} />
                    <Stack direction="row" spacing={2}>
                    <Button variant="contained" onClick={fetchProducts} sx={{flex: 2}}>Собрать статистику</Button>
                    <Button variant="contained" color="secondary" onClick={() => setSettingsModalOpen(true)} sx={{flex: 1}}>Изменить периодичности проверки</Button>
                    </Stack>
                    {loading && <CircularProgress />}
                    {error && <Typography color="error">{error}</Typography>}
                    {products.length > 0 && (
                        <>
                            <Typography variant="h6">Статистика</Typography>
                            <Typography>Товаров найдено: {stats.available}</Typography>
                            <Typography>Товаров отсутствует: {stats.not_available}</Typography>
                            <Button variant="outlined" onClick={downloadCSV}>Скачать отчет</Button>
                            <DataGrid rows={products} columns={columns} getRowId={(row) => row.prod_id} />
                        </>
                    )}
                </>
                :<Typography color="error">Выберите магазин</Typography>}
                {selectedStore && (
                <StoreSettingsModal
                    open={settingsModalOpen}
                    onClose={() => setSettingsModalOpen(false)}
                    storeId={selectedStore.id.toString()}
                    updateStoreCheckSettings={api.updateStoreCheckSettings}
                    onSuccess={() => {
                    // тут можно показать Snackbar или обновить данные
                    console.log("Настройки успешно обновлены");
                    }}
                />
                )}
            </Stack>
        </LocalizationProvider>
    );
};

export default ProductManagementPage;
