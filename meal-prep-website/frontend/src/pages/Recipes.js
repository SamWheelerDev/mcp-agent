import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  TextField,
  InputAdornment,
  CircularProgress,
  Pagination,
  Chip,
} from '@mui/material';
import {
  Search as SearchIcon,
  AccessTime as TimeIcon,
  Restaurant as MealIcon,
} from '@mui/icons-material';
import recipeService from '../services/recipeService';

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [totalRecipes, setTotalRecipes] = useState(0);
  const recipesPerPage = 6;

  // Fetch recipes on component mount and when search/page changes
  useEffect(() => {
    const fetchRecipes = async () => {
      setLoading(true);
      try {
        const response = await recipeService.getRecipes(
          searchTerm,
          page,
          recipesPerPage
        );
        setRecipes(response.recipes);
        setTotalRecipes(response.total);
        setError(null);
      } catch (err) {
        console.error('Error fetching recipes:', err);
        setError('Failed to load recipes. Please try again later.');
        setRecipes([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, [searchTerm, page]);

  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setPage(0); // Reset to first page when search changes
  };

  // Handle pagination change
  const handlePageChange = (event, value) => {
    setPage(value - 1); // API uses 0-based indexing
    window.scrollTo(0, 0); // Scroll to top when page changes
  };

  // Calculate total pages
  const totalPages = Math.ceil(totalRecipes / recipesPerPage);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Recipes
      </Typography>
      <Typography variant="body1" paragraph>
        Browse our collection of delicious and healthy recipes for your meal prep needs.
      </Typography>

      {/* Search Bar */}
      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search recipes..."
          value={searchTerm}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      {/* Recipes Grid */}
      {loading ? (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '50vh',
          }}
        >
          <CircularProgress />
        </Box>
      ) : error ? (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '50vh',
          }}
        >
          <Typography color="error">{error}</Typography>
        </Box>
      ) : recipes.length === 0 ? (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '50vh',
            flexDirection: 'column',
          }}
        >
          <Typography variant="h6" gutterBottom>
            No recipes found
          </Typography>
          <Typography variant="body1">
            Try adjusting your search or check back later for new recipes.
          </Typography>
        </Box>
      ) : (
        <>
          <Grid container spacing={4}>
            {recipes.map((recipe) => (
              <Grid item key={recipe.id} xs={12} sm={6} md={4}>
                <Card
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-5px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardMedia
                    component="img"
                    height="200"
                    image={recipe.image_url || 'https://via.placeholder.com/300x200?text=No+Image'}
                    alt={recipe.name}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {recipe.name}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: 'vertical',
                        mb: 2,
                      }}
                    >
                      {recipe.description}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip
                        icon={<TimeIcon />}
                        label={`Prep: ${recipe.prep_time} min`}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                      <Chip
                        icon={<TimeIcon />}
                        label={`Cook: ${recipe.cook_time} min`}
                        size="small"
                        color="secondary"
                        variant="outlined"
                      />
                    </Box>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      color="primary"
                      component={RouterLink}
                      to={`/recipes/${recipe.id}`}
                    >
                      View Recipe
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Pagination */}
          {totalPages > 1 && (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                mt: 4,
              }}
            >
              <Pagination
                count={totalPages}
                page={page + 1} // API uses 0-based indexing, but Pagination uses 1-based
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default Recipes;
