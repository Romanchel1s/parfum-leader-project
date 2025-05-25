import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';


const Header: React.FC = () => {
    const navigate = useNavigate();
    return (
        <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
            <Toolbar>
                <Button color="inherit" onClick={() => navigate('/')}>
                <Typography variant="h6" component="div">
                    Admin Panel
                </Typography>
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
