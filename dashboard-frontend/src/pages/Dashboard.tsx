import { List, ListItem, Stack, Typography } from '@mui/material';
import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  return (
      <Stack 
        sx={{ 
          alignItems: 'center',
          height: '90vh',
          justifyContent: 'center',
          backgroundColor: '#f9f9f9',
        }}
      >
        <Typography 
          variant='h1' 
          sx={{ 
            fontSize: '2.5rem', 
            fontWeight: 'bold', 
            color: '#333', 
            marginBottom: '20px' 
          }}
        >
          Admin Panel Dashboard
        </Typography>
        <List 
          sx={{ 
            width: '100%', 
            maxWidth: '400px', 
            backgroundColor: '#fff', 
            borderRadius: '8px', 
            boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)' 
          }}
        >
          <ListItem 
            sx={{ 
              '&:hover': { backgroundColor: '#f0f0f0' } 
            }}
          >
            <Link 
              to="/employee-management" 
              style={{ 
                textDecoration: 'none', 
                color: '#007bff', 
                fontWeight: '500' 
              }}
            >
              Employee Management
            </Link>
          </ListItem>
          <ListItem 
            sx={{ 
              '&:hover': { backgroundColor: '#f0f0f0' } 
            }}
          >
            <Link 
              to="/products" 
              style={{ 
                textDecoration: 'none', 
                color: '#007bff', 
                fontWeight: '500' 
              }}
            >
              Product Management
            </Link>
          </ListItem>
        </List>
      </Stack>
  );
};

export default Dashboard;
