import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Paper,
  Container,
  CircularProgress,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
  FormControlLabel,
  Checkbox,
  Slider,
  Grid,
  Alert,
} from '@mui/material';
import onboardingService from '../services/onboardingService';

// Step components
const WelcomeStep = ({ onNext }) => (
  <Box>
    <Typography variant="h5" gutterBottom>
      Welcome to Meal Prep Assistant!
    </Typography>
    <Typography paragraph>
      We're excited to help you plan and prepare delicious meals tailored to your preferences.
      Let's take a few moments to understand your tastes and cooking habits.
    </Typography>
    <Typography paragraph>
      This quick onboarding process will help us personalize your experience and provide
      recommendations that match your dietary needs and preferences.
    </Typography>
    <Button variant="contained" color="primary" onClick={onNext}>
      Let's Get Started
    </Button>
  </Box>
);

const DietaryRestrictionsStep = ({ onNext, onPrevious, onSave, initialData = {} }) => {
  const [restrictions, setRestrictions] = useState({
    vegetarian: initialData.vegetarian || false,
    vegan: initialData.vegan || false,
    glutenFree: initialData.glutenFree || false,
    dairyFree: initialData.dairyFree || false,
    nutFree: initialData.nutFree || false,
    lowCarb: initialData.lowCarb || false,
  });
  const [allergies, setAllergies] = useState(initialData.allergies || '');

  const handleChange = (event) => {
    setRestrictions({
      ...restrictions,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSave = () => {
    onSave({
      ...restrictions,
      allergies,
    });
    onNext();
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Dietary Restrictions
      </Typography>
      <Typography paragraph>
        Let us know about any dietary restrictions or allergies you have.
        This helps us recommend recipes that match your needs.
      </Typography>

      <FormControl component="fieldset" sx={{ mb: 3 }}>
        <FormLabel component="legend">Select any that apply:</FormLabel>
        <Grid container spacing={2}>
          {Object.entries(restrictions).map(([key, value]) => (
            <Grid item xs={6} key={key}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={value}
                    onChange={handleChange}
                    name={key}
                  />
                }
                label={key.replace(/([A-Z])/g, ' $1').replace(/^./, (str) => str.toUpperCase())}
              />
            </Grid>
          ))}
        </Grid>
      </FormControl>

      <TextField
        fullWidth
        label="Any specific food allergies?"
        multiline
        rows={2}
        value={allergies}
        onChange={(e) => setAllergies(e.target.value)}
        placeholder="e.g., shellfish, peanuts, etc."
        sx={{ mb: 3 }}
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button onClick={onPrevious}>Back</Button>
        <Button variant="contained" color="primary" onClick={handleSave}>
          Continue
        </Button>
      </Box>
    </Box>
  );
};

const TastePreferencesStep = ({ onNext, onPrevious, onSave, initialData = {} }) => {
  const [preferences, setPreferences] = useState({
    spicy: initialData.spicy || 3,
    sweet: initialData.sweet || 3,
    savory: initialData.savory || 3,
    bitter: initialData.bitter || 3,
    sour: initialData.sour || 3,
  });

  const handleChange = (name) => (event, newValue) => {
    setPreferences({
      ...preferences,
      [name]: newValue,
    });
  };

  const handleSave = () => {
    onSave(preferences);
    onNext();
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Taste Preferences
      </Typography>
      <Typography paragraph>
        Everyone has different taste preferences. Help us understand yours by rating how much you enjoy
        each of these flavor profiles.
      </Typography>

      {Object.entries(preferences).map(([key, value]) => (
        <Box key={key} sx={{ mb: 3 }}>
          <Typography id={`${key}-slider`} gutterBottom>
            {key.charAt(0).toUpperCase() + key.slice(1)}
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs>
              <Slider
                value={value}
                onChange={handleChange(key)}
                aria-labelledby={`${key}-slider`}
                valueLabelDisplay="auto"
                step={1}
                marks
                min={1}
                max={5}
              />
            </Grid>
            <Grid item>
              <Typography>{value}</Typography>
            </Grid>
          </Grid>
        </Box>
      ))}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button onClick={onPrevious}>Back</Button>
        <Button variant="contained" color="primary" onClick={handleSave}>
          Continue
        </Button>
      </Box>
    </Box>
  );
};

const CookingHabitsStep = ({ onNext, onPrevious, onSave, initialData = {} }) => {
  const [frequency, setFrequency] = useState(initialData.frequency || 'few-times-week');
  const [experience, setExperience] = useState(initialData.experience || 'intermediate');
  const [mealPrepDay, setMealPrepDay] = useState(initialData.mealPrepDay || 'sunday');

  const handleSave = () => {
    onSave({
      frequency,
      experience,
      mealPrepDay,
    });
    onNext();
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Cooking Habits
      </Typography>
      <Typography paragraph>
        Tell us about your cooking routine so we can suggest recipes that fit your lifestyle.
      </Typography>

      <FormControl component="fieldset" sx={{ mb: 3 }}>
        <FormLabel component="legend">How often do you cook?</FormLabel>
        <RadioGroup
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
        >
          <FormControlLabel value="daily" control={<Radio />} label="Daily" />
          <FormControlLabel value="few-times-week" control={<Radio />} label="A few times a week" />
          <FormControlLabel value="weekends" control={<Radio />} label="Weekends only" />
          <FormControlLabel value="rarely" control={<Radio />} label="Rarely" />
        </RadioGroup>
      </FormControl>

      <FormControl component="fieldset" sx={{ mb: 3 }}>
        <FormLabel component="legend">What's your cooking experience level?</FormLabel>
        <RadioGroup
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
        >
          <FormControlLabel value="beginner" control={<Radio />} label="Beginner" />
          <FormControlLabel value="intermediate" control={<Radio />} label="Intermediate" />
          <FormControlLabel value="advanced" control={<Radio />} label="Advanced" />
          <FormControlLabel value="professional" control={<Radio />} label="Professional" />
        </RadioGroup>
      </FormControl>

      <FormControl component="fieldset" sx={{ mb: 3 }}>
        <FormLabel component="legend">Preferred day for meal prep?</FormLabel>
        <RadioGroup
          value={mealPrepDay}
          onChange={(e) => setMealPrepDay(e.target.value)}
        >
          <FormControlLabel value="sunday" control={<Radio />} label="Sunday" />
          <FormControlLabel value="monday" control={<Radio />} label="Monday" />
          <FormControlLabel value="saturday" control={<Radio />} label="Saturday" />
          <FormControlLabel value="no-preference" control={<Radio />} label="No preference" />
        </RadioGroup>
      </FormControl>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button onClick={onPrevious}>Back</Button>
        <Button variant="contained" color="primary" onClick={handleSave}>
          Continue
        </Button>
      </Box>
    </Box>
  );
};

const OnboardingComplete = ({ onFinish }) => (
  <Box sx={{ textAlign: 'center' }}>
    <Typography variant="h5" gutterBottom>
      Onboarding Complete!
    </Typography>
    <Typography paragraph>
      Thank you for sharing your preferences with us. We'll use this information to personalize
      your meal recommendations and planning experience.
    </Typography>
    <Typography paragraph>
      You're all set to start exploring recipes and planning your meals!
    </Typography>
    <Button variant="contained" color="primary" onClick={onFinish}>
      Get Started
    </Button>
  </Box>
);

// Main Onboarding Component
const Onboarding = () => {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stepData, setStepData] = useState({});
  const [steps, setSteps] = useState([]);

  useEffect(() => {
    const fetchOnboardingState = async () => {
      try {
        setLoading(true);
        // Start or resume onboarding
        const response = await onboardingService.getCurrentStep(userId);
        
        if (response.current_step) {
          // Find the step index
          const stepIndex = steps.findIndex(step => step.id === response.current_step.id);
          if (stepIndex >= 0) {
            setActiveStep(stepIndex);
          }
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching onboarding state:', err);
        setError('Failed to load onboarding. Please try again later.');
        setLoading(false);
      }
    };

    // Define the steps
    setSteps([
      { id: 'welcome', title: 'Welcome', component: WelcomeStep },
      { id: 'dietary_restrictions', title: 'Dietary Restrictions', component: DietaryRestrictionsStep },
      { id: 'taste_preferences', title: 'Taste Preferences', component: TastePreferencesStep },
      { id: 'cooking_habits', title: 'Cooking Habits', component: CookingHabitsStep },
    ]);

    if (userId) {
      fetchOnboardingState();
    } else {
      setLoading(false);
    }
  }, [userId, steps]);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStepSave = async (stepId, data) => {
    try {
      setStepData({
        ...stepData,
        [stepId]: data,
      });
      
      if (userId) {
        await onboardingService.processStep(userId, stepId, data);
      }
    } catch (err) {
      console.error(`Error saving step ${stepId}:`, err);
      setError(`Failed to save your preferences. Please try again.`);
    }
  };

  const handleFinish = async () => {
    try {
      if (userId) {
        await onboardingService.completeOnboarding(userId);
      }
      navigate('/');
    } catch (err) {
      console.error('Error completing onboarding:', err);
      setError('Failed to complete onboarding. Please try again.');
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
        <CircularProgress />
      </Container>
    );
  }

  const CurrentStepComponent = activeStep < steps.length 
    ? steps[activeStep].component 
    : OnboardingComplete;

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 4 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((step) => (
            <Step key={step.id}>
              <StepLabel>{step.title}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <CurrentStepComponent
          onNext={handleNext}
          onPrevious={handleBack}
          onSave={(data) => handleStepSave(steps[activeStep]?.id, data)}
          onFinish={handleFinish}
          initialData={stepData[steps[activeStep]?.id]}
        />
      </Paper>
    </Container>
  );
};

export default Onboarding;
