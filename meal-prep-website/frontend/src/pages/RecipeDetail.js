import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  AccessTime as TimeIcon,
  ArrowBack as ArrowBackIcon,
  CheckCircle as CheckCircleIcon,
  FiberManualRecord as BulletIcon,
} from '@mui/icons-material';
import recipeService from '../services/recipeService';

const RecipeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipe = async () => {
      setLoading(true);
      try {
        const data = await recipeService.getRecipe(id);
        setRecipe(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching recipe:', err);
        setError('Failed to load recipe. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [id]);

  // Parse ingredients into an array
  const parseIngredients = (ingredientsString) => {
    if (!ingredientsString) return [];
    return ingredientsString.split(',').map((item) => item.trim());
  };

  // Parse instructions into an array
  const parseInstructions = (instructionsString) => {
    if (!instructionsString) return [];
    return instructionsString
      .split(/\d+\./)
      .filter((item) => item.trim().length > 0)
      .map((item) => item.trim());
  };

  // Handle back button click
  const handleBack = () => {
    navigate('/recipes');
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '80vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
        >
          Back to Recipes
        </Button>
      </Container>
    );
  }

  if (!recipe) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="warning" sx={{ mb: 2 }}>
          Recipe not found
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
        >
          Back to Recipes
        </Button>
      </Container>
    );
  }

  const ingredients = parseIngredients(recipe.ingredients);
  const instructions = parseInstructions(recipe.instructions);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={handleBack}
        sx={{ mb: 3 }}
      >
        Back to Recipes
      </Button>

      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={4}>
          {/* Recipe Image */}
          <Grid item xs={12} md={6}>
            <Box
              component="img"
              src={recipe.image_url || 'https://via.placeholder.com/600x400?text=No+Image'}
              alt={recipe.name}
              sx={{
                width: '100%',
                height: 'auto',
                borderRadius: 2,
                boxShadow: 2,
              }}
            />
          </Grid>

          {/* Recipe Info */}
          <Grid item xs={12} md={6}>
            <Typography variant="h4" component="h1" gutterBottom>
              {recipe.name}
            </Typography>
            <Typography variant="body1" paragraph>
              {recipe.description}
            </Typography>

            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Chip
                icon={<TimeIcon />}
                label={`Prep: ${recipe.prep_time} min`}
                color="primary"
              />
              <Chip
                icon={<TimeIcon />}
                label={`Cook: ${recipe.cook_time} min`}
                color="secondary"
              />
              <Chip
                label={`Total: ${recipe.prep_time + recipe.cook_time} min`}
                variant="outlined"
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Grid container spacing={4}>
        {/* Ingredients */}
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Ingredients
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <List>
              {ingredients.map((ingredient, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <BulletIcon color="primary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={ingredient} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Instructions */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Instructions
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <List>
              {instructions.map((instruction, index) => (
                <ListItem key={index} alignItems="flex-start" sx={{ py: 1 }}>
                  <ListItemIcon>
                    <Typography
                      variant="h6"
                      component="span"
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 28,
                        height: 28,
                        borderRadius: '50%',
                        bgcolor: 'primary.main',
                        color: 'white',
                      }}
                    >
                      {index + 1}
                    </Typography>
                  </ListItemIcon>
                  <ListItemText primary={instruction} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default RecipeDetail;
