import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Link,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Restaurant as RecipeIcon,
  CalendarMonth as CalendarIcon,
} from '@mui/icons-material';

const Home = () => {
  const features = [
    {
      title: 'Chat with Assistant',
      description:
        'Get personalized meal suggestions, cooking tips, and answers to your food-related questions.',
      icon: <ChatIcon fontSize="large" color="primary" />,
      link: '/chat',
      image: 'https://images.unsplash.com/photo-1577563908411-5077b6dc7624?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2hhdHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60',
    },
    {
      title: 'Discover Recipes',
      description:
        'Browse through a collection of delicious and healthy recipes for your meal prep needs.',
      icon: <RecipeIcon fontSize="large" color="primary" />,
      link: '/recipes',
      image: 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cmVjaXBlfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60',
    },
    {
      title: 'Plan Your Week',
      description:
        'Organize your meals for the week with our easy-to-use calendar planning tool.',
      icon: <CalendarIcon fontSize="large" color="primary" />,
      link: '/calendar',
      image: 'https://images.unsplash.com/photo-1506784365847-bbad939e9335?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2FsZW5kYXJ8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60',
    },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          mb: 6,
        }}
      >
        <Container maxWidth="lg">
          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 'bold' }}
          >
            Meal Prep Made Easy
          </Typography>
          <Typography variant="h5" paragraph sx={{ mb: 4, maxWidth: '800px' }}>
            Plan your meals, discover new recipes, and simplify your cooking routine with our
            intelligent meal prep assistant.
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            component={RouterLink}
            to="/chat"
            sx={{ mr: 2 }}
          >
            Start Chatting
          </Button>
          <Button
            variant="outlined"
            color="inherit"
            size="large"
            component={RouterLink}
            to="/recipes"
          >
            Browse Recipes
          </Button>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography
          variant="h3"
          component="h2"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Features
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature) => (
            <Grid item xs={12} md={4} key={feature.title}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={feature.image}
                  alt={feature.title}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    {feature.icon}
                    <Typography variant="h5" component="h3" sx={{ ml: 1 }}>
                      {feature.title}
                    </Typography>
                  </Box>
                  <Typography variant="body1">{feature.description}</Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    color="primary"
                    component={RouterLink}
                    to={feature.link}
                  >
                    Learn More
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* How It Works Section */}
      <Box sx={{ bgcolor: 'grey.100', py: 8, mb: 8 }}>
        <Container maxWidth="lg">
          <Typography
            variant="h3"
            component="h2"
            align="center"
            gutterBottom
            sx={{ mb: 6 }}
          >
            How It Works
          </Typography>
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" component="h3" gutterBottom>
                  1. Chat
                </Typography>
                <Typography variant="body1">
                  Tell our assistant about your dietary preferences, available ingredients,
                  and meal prep goals.
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" component="h3" gutterBottom>
                  2. Discover
                </Typography>
                <Typography variant="body1">
                  Get personalized recipe recommendations and meal planning suggestions.
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" component="h3" gutterBottom>
                  3. Plan
                </Typography>
                <Typography variant="body1">
                  Organize your weekly meals with our calendar tool and simplify your
                  cooking routine.
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Call to Action */}
      <Container maxWidth="md" sx={{ textAlign: 'center', mb: 8 }}>
        <Typography variant="h3" component="h2" gutterBottom>
          Ready to simplify your meal planning?
        </Typography>
        <Typography variant="h6" paragraph sx={{ mb: 4 }}>
          Start using our Meal Prep Assistant today and take the stress out of cooking.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          component={RouterLink}
          to="/chat"
        >
          Get Started
        </Button>
      </Container>
    </Box>
  );
};

export default Home;
