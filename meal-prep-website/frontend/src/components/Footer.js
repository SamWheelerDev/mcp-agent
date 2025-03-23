import React from 'react';
import { Box, Container, Typography, Link, Divider } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[100],
      }}
    >
      <Divider sx={{ mb: 3 }} />
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, justifyContent: 'space-between' }}>
          <Box sx={{ mb: { xs: 2, md: 0 } }}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Meal Prep Assistant
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Plan your meals, discover recipes, and simplify your cooking
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Quick Links
            </Typography>
            <Link href="/" color="inherit" underline="hover">
              Home
            </Link>
            <Link href="/chat" color="inherit" underline="hover">
              Chat
            </Link>
            <Link href="/recipes" color="inherit" underline="hover">
              Recipes
            </Link>
            <Link href="/calendar" color="inherit" underline="hover">
              Calendar
            </Link>
          </Box>
        </Box>
        
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            {'© '}
            {new Date().getFullYear()}
            {' Meal Prep Assistant. All rights reserved.'}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
