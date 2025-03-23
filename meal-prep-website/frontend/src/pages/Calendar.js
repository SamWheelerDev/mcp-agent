import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Button,
  Card,
  CardContent,
  CardActions,
  IconButton,
  Divider,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tooltip,
  Snackbar,
} from '@mui/material';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { format, addDays, startOfWeek, addWeeks, subWeeks, isSameDay } from 'date-fns';
import calendarService from '../services/calendarService';
import recipeService from '../services/recipeService';

const Calendar = ({ user }) => {
  const [mealPlans, setMealPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentWeekStart, setCurrentWeekStart] = useState(startOfWeek(new Date()));
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [mealPlanToDelete, setMealPlanToDelete] = useState(null);

  // Fetch meal plans for the current week
  useEffect(() => {
    const fetchMealPlans = async () => {
      setLoading(true);
      try {
        const startDate = format(currentWeekStart, 'yyyy-MM-dd');
        const endDate = format(addDays(currentWeekStart, 6), 'yyyy-MM-dd');
        
        const response = await calendarService.getMealPlans(
          user.id,
          startDate,
          endDate
        );
        
        setMealPlans(response.meal_plans);
        setError(null);
      } catch (err) {
        console.error('Error fetching meal plans:', err);
        setError('Failed to load meal plans. Please try again later.');
        setMealPlans([]);
      } finally {
        setLoading(false);
      }
    };

    fetchMealPlans();
  }, [user.id, currentWeekStart]);

  // Generate days of the week
  const weekDays = Array.from({ length: 7 }, (_, i) => {
    const day = addDays(currentWeekStart, i);
    return {
      date: day,
      dayName: format(day, 'EEEE'),
      dayMonth: format(day, 'MMM d'),
      isToday: isSameDay(day, new Date()),
    };
  });

  // Navigate to previous week
  const handlePreviousWeek = () => {
    setCurrentWeekStart(subWeeks(currentWeekStart, 1));
  };

  // Navigate to next week
  const handleNextWeek = () => {
    setCurrentWeekStart(addWeeks(currentWeekStart, 1));
  };

  // Generate a weekly meal plan
  const handleGenerateWeeklyPlan = async () => {
    setGeneratingPlan(true);
    try {
      const startDate = format(currentWeekStart, 'yyyy-MM-dd');
      const response = await calendarService.generateWeeklyPlan(user.id, startDate);
      setMealPlans(response.meal_plans);
      setSnackbarMessage('Weekly meal plan generated successfully!');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error generating meal plan:', err);
      setSnackbarMessage('Failed to generate meal plan. Please try again.');
      setSnackbarOpen(true);
    } finally {
      setGeneratingPlan(false);
    }
  };

  // Open confirm dialog for deleting a meal plan
  const handleDeleteClick = (mealPlan) => {
    setMealPlanToDelete(mealPlan);
    setConfirmDialogOpen(true);
  };

  // Delete a meal plan
  const handleConfirmDelete = async () => {
    if (!mealPlanToDelete) return;
    
    try {
      await calendarService.deleteMealPlan(mealPlanToDelete.id);
      setMealPlans(mealPlans.filter(mp => mp.id !== mealPlanToDelete.id));
      setSnackbarMessage('Meal plan deleted successfully!');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error deleting meal plan:', err);
      setSnackbarMessage('Failed to delete meal plan. Please try again.');
      setSnackbarOpen(true);
    } finally {
      setConfirmDialogOpen(false);
      setMealPlanToDelete(null);
    }
  };

  // Close confirm dialog
  const handleCancelDelete = () => {
    setConfirmDialogOpen(false);
    setMealPlanToDelete(null);
  };

  // Close snackbar
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  // Get meal plans for a specific day and meal type
  const getMealPlan = (date, mealType) => {
    const dateString = format(date, 'yyyy-MM-dd');
    return mealPlans.find(
      (mp) => format(new Date(mp.plan_date), 'yyyy-MM-dd') === dateString && mp.meal_type === mealType
    );
  };

  // Meal types
  const mealTypes = ['breakfast', 'lunch', 'dinner'];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Meal Planning Calendar
        </Typography>
        <Box>
          <Button
            variant="contained"
            color="primary"
            startIcon={<RefreshIcon />}
            onClick={handleGenerateWeeklyPlan}
            disabled={generatingPlan}
            sx={{ mr: 2 }}
          >
            {generatingPlan ? 'Generating...' : 'Generate Weekly Plan'}
          </Button>
        </Box>
      </Box>

      {/* Week Navigation */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Button
          startIcon={<ChevronLeftIcon />}
          onClick={handlePreviousWeek}
        >
          Previous Week
        </Button>
        <Typography variant="h6">
          {format(currentWeekStart, 'MMMM d')} - {format(addDays(currentWeekStart, 6), 'MMMM d, yyyy')}
        </Typography>
        <Button
          endIcon={<ChevronRightIcon />}
          onClick={handleNextWeek}
        >
          Next Week
        </Button>
      </Box>

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
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      ) : (
        <Grid container spacing={2}>
          {weekDays.map((day) => (
            <Grid item xs={12} key={day.dayName}>
              <Paper
                elevation={2}
                sx={{
                  p: 2,
                  bgcolor: day.isToday ? 'primary.light' : 'background.paper',
                  color: day.isToday ? 'white' : 'inherit',
                }}
              >
                <Typography variant="h6" sx={{ mb: 1 }}>
                  {day.dayName} ({day.dayMonth})
                </Typography>
                <Divider sx={{ mb: 2 }} />

                <Grid container spacing={2}>
                  {mealTypes.map((mealType) => {
                    const mealPlan = getMealPlan(day.date, mealType);
                    
                    return (
                      <Grid item xs={12} md={4} key={mealType}>
                        <Card
                          variant="outlined"
                          sx={{
                            height: '100%',
                            display: 'flex',
                            flexDirection: 'column',
                          }}
                        >
                          <CardContent sx={{ flexGrow: 1 }}>
                            <Typography
                              variant="subtitle1"
                              sx={{ mb: 1, textTransform: 'capitalize' }}
                            >
                              {mealType}
                            </Typography>
                            
                            {mealPlan ? (
                              <>
                                <Typography variant="h6" gutterBottom>
                                  {mealPlan.recipe_name}
                                </Typography>
                                <Typography
                                  variant="body2"
                                  color="text.secondary"
                                  sx={{
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    display: '-webkit-box',
                                    WebkitLineClamp: 2,
                                    WebkitBoxOrient: 'vertical',
                                  }}
                                >
                                  {mealPlan.recipe_description}
                                </Typography>
                              </>
                            ) : (
                              <Typography variant="body2" color="text.secondary">
                                No meal planned
                              </Typography>
                            )}
                          </CardContent>
                          
                          <CardActions>
                            {mealPlan ? (
                              <>
                                <Button
                                  size="small"
                                  component={RouterLink}
                                  to={`/recipes/${mealPlan.recipe_id}`}
                                >
                                  View Recipe
                                </Button>
                                <Box sx={{ flexGrow: 1 }} />
                                <Tooltip title="Remove meal">
                                  <IconButton
                                    size="small"
                                    color="error"
                                    onClick={() => handleDeleteClick(mealPlan)}
                                  >
                                    <DeleteIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              </>
                            ) : (
                              <Button
                                size="small"
                                startIcon={<AddIcon />}
                                component={RouterLink}
                                to="/recipes"
                              >
                                Add Meal
                              </Button>
                            )}
                          </CardActions>
                        </Card>
                      </Grid>
                    );
                  })}
                </Grid>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Confirm Delete Dialog */}
      <Dialog open={confirmDialogOpen} onClose={handleCancelDelete}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to remove{' '}
            {mealPlanToDelete?.recipe_name || 'this meal'} from your meal plan?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete}>Cancel</Button>
          <Button onClick={handleConfirmDelete} color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        message={snackbarMessage}
      />
    </Container>
  );
};

export default Calendar;
