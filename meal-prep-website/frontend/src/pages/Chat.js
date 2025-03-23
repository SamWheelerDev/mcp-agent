import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  Avatar,
  CircularProgress,
  Divider,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import chatService from '../services/chatService';

const Chat = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const messagesEndRef = useRef(null);

  // Fetch chat history on component mount
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await chatService.getChatHistory(user.id);
        // Reverse to show newest messages at the bottom
        const sortedMessages = response.messages.sort(
          (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
        );
        setMessages(sortedMessages);
        setInitialLoading(false);
      } catch (error) {
        console.error('Error fetching chat history:', error);
        setInitialLoading(false);
      }
    };

    fetchChatHistory();
  }, [user.id]);

  // Scroll to bottom of messages when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    // Optimistically add user message to UI
    const userMessage = {
      id: Date.now(), // Temporary ID
      user_id: user.id,
      message: newMessage,
      response: '',
      timestamp: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setNewMessage('');
    setLoading(true);

    try {
      // Send message to API
      const response = await chatService.sendMessage(user.id, newMessage);
      
      // Update messages with the actual response
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === userMessage.id ? response : msg
        )
      );
    } catch (error) {
      console.error('Error sending message:', error);
      // Show error in UI
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === userMessage.id
            ? {
                ...msg,
                response:
                  'Sorry, there was an error processing your request. Please try again.',
              }
            : msg
        )
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Chat with Meal Prep Assistant
      </Typography>
      <Typography variant="body1" paragraph>
        Ask about recipes, meal planning, cooking tips, or dietary advice.
      </Typography>

      <Paper
        elevation={3}
        sx={{
          height: '60vh',
          display: 'flex',
          flexDirection: 'column',
          mb: 2,
        }}
      >
        {initialLoading ? (
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <List
            sx={{
              width: '100%',
              bgcolor: 'background.paper',
              overflow: 'auto',
              flexGrow: 1,
              p: 2,
            }}
          >
            {messages.length === 0 ? (
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: '100%',
                  flexDirection: 'column',
                }}
              >
                <Typography variant="body1" color="text.secondary" align="center">
                  No messages yet. Start the conversation by asking about meal planning,
                  recipes, or cooking tips.
                </Typography>
              </Box>
            ) : (
              messages.map((msg, index) => (
                <React.Fragment key={msg.id || index}>
                  {/* User message */}
                  <ListItem alignItems="flex-start" sx={{ flexDirection: 'row-reverse' }}>
                    <Avatar sx={{ ml: 2, bgcolor: 'primary.main' }}>
                      {user.username.charAt(0).toUpperCase()}
                    </Avatar>
                    <ListItemText
                      primary={
                        <Typography
                          sx={{ display: 'inline', fontWeight: 'bold' }}
                          component="span"
                          variant="body1"
                          color="text.primary"
                        >
                          You
                        </Typography>
                      }
                      secondary={
                        <Typography
                          sx={{ display: 'inline' }}
                          component="span"
                          variant="body1"
                          color="text.primary"
                        >
                          {msg.message}
                        </Typography>
                      }
                      sx={{
                        bgcolor: 'primary.light',
                        p: 2,
                        borderRadius: 2,
                        color: 'white',
                      }}
                    />
                  </ListItem>

                  {/* Assistant response */}
                  {msg.response && (
                    <ListItem alignItems="flex-start">
                      <Avatar sx={{ mr: 2, bgcolor: 'secondary.main' }}>AI</Avatar>
                      <ListItemText
                        primary={
                          <Typography
                            sx={{ display: 'inline', fontWeight: 'bold' }}
                            component="span"
                            variant="body1"
                            color="text.primary"
                          >
                            Assistant
                          </Typography>
                        }
                        secondary={
                          <Typography
                            sx={{ display: 'inline', whiteSpace: 'pre-wrap' }}
                            component="span"
                            variant="body1"
                            color="text.primary"
                          >
                            {msg.response}
                          </Typography>
                        }
                        sx={{
                          bgcolor: 'grey.100',
                          p: 2,
                          borderRadius: 2,
                        }}
                      />
                    </ListItem>
                  )}

                  {/* Loading indicator for waiting for response */}
                  {loading && index === messages.length - 1 && !msg.response && (
                    <ListItem alignItems="flex-start">
                      <Avatar sx={{ mr: 2, bgcolor: 'secondary.main' }}>AI</Avatar>
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          bgcolor: 'grey.100',
                          p: 2,
                          borderRadius: 2,
                        }}
                      >
                        <CircularProgress size={20} sx={{ mr: 2 }} />
                        <Typography variant="body1" color="text.secondary">
                          Thinking...
                        </Typography>
                      </Box>
                    </ListItem>
                  )}

                  <Divider component="li" sx={{ my: 2 }} />
                </React.Fragment>
              ))
            )}
            <div ref={messagesEndRef} />
          </List>
        )}

        <Divider />

        <Box
          component="form"
          onSubmit={handleSendMessage}
          sx={{
            p: 2,
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            disabled={loading}
            sx={{ mr: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            endIcon={<SendIcon />}
            disabled={loading || !newMessage.trim()}
          >
            Send
          </Button>
        </Box>
      </Paper>

      <Typography variant="body2" color="text.secondary">
        Try asking about meal prep ideas, specific dietary needs, or cooking techniques.
      </Typography>
    </Container>
  );
};

export default Chat;
