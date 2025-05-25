import { Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const ProductNavigationPage = () => {
    const navigate = useNavigate();

    return (
        <Stack spacing={3} sx={{ width: "50%", margin: "auto", marginTop: 4, textAlign: "center" }}>
            <Typography variant="h4">Выберите действие</Typography>
            <Button variant="contained" onClick={() => navigate("/products")}>Статистика по каждому товару</Button>
            <Button variant="outlined" onClick={() => navigate("/another-page")}>статистика по конкретному товару</Button>
        </Stack>
    );
};

export default ProductNavigationPage;
