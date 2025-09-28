import React, { useState, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Image,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as Speech from "expo-speech";
import { LinearGradient } from "expo-linear-gradient";
import { Audio } from 'expo-av'; 

type Message = {
  id: string;
  sender: "user" | "ai";
  text?: string;
  imageUri?: string;
  voiceUri?: string;
  createdAt: number;
};

type ComposingMessage = {
  text: string;
  imageUri?: string;
  voiceUri?: string;
};

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [composingMessage, setComposingMessage] = useState<ComposingMessage>({ text: "" });
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [playingVoice, setPlayingVoice] = useState<string | null>(null);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);

  const addMessage = (msg: Message) => {
    setMessages((prev) => [...prev, msg]);
    // Auto-scroll to bottom
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);
  };

  const handleSend = () => {
    // Only send if there's text, image, or voice
    if (!composingMessage.text.trim() && !composingMessage.imageUri && !composingMessage.voiceUri) {
      return;
    }

    addMessage({
      id: Date.now().toString(),
      sender: "user",
      text: composingMessage.text.trim() || undefined,
      imageUri: composingMessage.imageUri,
      voiceUri: composingMessage.voiceUri,
      createdAt: Date.now(),
    });

    // Reset composing message
    setComposingMessage({ text: "" });
    
    // Simulate AI response
    setTimeout(() => {
      addMessage({
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: "Thank you for your message! I'm here to help with your farming questions. How can I assist you today?",
        createdAt: Date.now(),
      });
    }, 1000);
  };

  // 🎤 Start voice recording
  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status !== 'granted') {
        Alert.alert('Permission required', 'Please grant microphone permission to record voice messages.');
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error('Failed to start recording', err);
      Alert.alert('Error', 'Failed to start recording');
    }
  };

  // 🎤 Stop voice recording
  const stopRecording = async () => {
    if (!recording) return;
    
    try {
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      
      if (uri) {
        setComposingMessage(prev => ({
          ...prev,
          voiceUri: uri
        }));
      }
      
      setRecording(null);
    } catch (err) {
      console.error('Failed to stop recording', err);
    }
  };


  const speakText = (text: string) => {
    if (isSpeaking) {
      Speech.stop();
      setIsSpeaking(false);
    } else {
      Speech.speak(text, {
        language: 'en',
        pitch: 1,
        rate: 0.8,
      });
      setIsSpeaking(true);
      
      // Poll every 500ms to check if speaking is done
      const checkSpeaking = setInterval(() => {
        Speech.isSpeakingAsync().then((status) => {
          if (!status) {
            setIsSpeaking(false);
            clearInterval(checkSpeaking);
          }
        });
      }, 500);
    }
  };

  // 🔊 Play voice message
  const playVoiceMessage = async (voiceUri: string) => {
    try {
      // Stop any currently playing sound
      if (sound) {
        await sound.unloadAsync();
        setSound(null);
      }

      // If clicking the same voice message, stop it
      if (playingVoice === voiceUri) {
        setPlayingVoice(null);
        return;
      }

      // Load and play the new voice message
      const { sound: newSound } = await Audio.Sound.createAsync(
        { uri: voiceUri },
        { shouldPlay: true }
      );
      
      setSound(newSound);
      setPlayingVoice(voiceUri);

      // Set up playback status listener
      newSound.setOnPlaybackStatusUpdate((status) => {
        if (status.isLoaded && status.didJustFinish) {
          setPlayingVoice(null);
          setSound(null);
        }
      });
    } catch (error) {
      console.error('Error playing voice message:', error);
      Alert.alert('Error', 'Failed to play voice message');
    }
  };

  const pickImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (permission.status !== 'granted') {
      Alert.alert('Permission required', 'Please grant camera roll permission to select images.');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
      allowsEditing: true,
      aspect: [4, 3],
    });

    if (!result.canceled) {
      setComposingMessage(prev => ({
        ...prev,
        imageUri: result.assets[0].uri
      }));
    }
  };

  const takePhoto = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (permission.status !== 'granted') {
      Alert.alert('Permission required', 'Please grant camera permission to take photos.');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
      allowsEditing: true,
      aspect: [4, 3],
    });

    if (!result.canceled) {
      setComposingMessage(prev => ({
        ...prev,
        imageUri: result.assets[0].uri
      }));
    }
  };

  const renderMessage = (item: Message) => (
    <View
      key={item.id}
      className={`mb-4 max-w-[80%] ${
        item.sender === "user" ? "self-end" : "self-start"
      }`}
    >
      <View
        className={`px-4 py-3 rounded-2xl ${
          item.sender === "user"
            ? "bg-green-500"
            : "bg-gray-100"
        }`}
      >
        {item.text && (
          <Text
            className={`text-base ${
              item.sender === "user" ? "text-white" : "text-gray-800"
            }`}
          >
            {item.text}
          </Text>
        )}
        {item.imageUri && (
          <Image
            source={{ uri: item.imageUri }}
            className="w-48 h-48 mt-2 rounded-lg"
            resizeMode="cover"
          />
        )}
        {item.voiceUri && (
          <TouchableOpacity 
            onPress={() => playVoiceMessage(item.voiceUri!)}
            className="flex-row items-center mt-2"
          >
            <Text className={`text-sm ${item.sender === "user" ? "text-green-100" : "text-gray-600"}`}>
              {playingVoice === item.voiceUri ? "⏸️ Playing..." : "🎤 Tap to play"}
            </Text>
          </TouchableOpacity>
        )}
      </View>
      
      {/* AI message actions */}
      {item.sender === "ai" && item.text && (
        <TouchableOpacity
          onPress={() => speakText(item.text!)}
          className="mt-2 self-start"
        >
          <Text className="text-green-600 text-sm">
            {isSpeaking ? "🔊 Stop" : "🔊 Listen"}
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );

  return (
    <KeyboardAvoidingView 
      className="flex-1 bg-gray-50" 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <Text className="text-white text-2xl font-bold mb-2 mt-5">AI Farming Assistant</Text>
        <Text className="text-green-100 text-base">Ask questions, share photos, or use voice chat</Text>
      </LinearGradient>

      {/* Messages Area */}
      <ScrollView
        ref={scrollViewRef}
        className="flex-1 px-4 py-4"
        showsVerticalScrollIndicator={false}
      >
        {messages.length === 0 ? (
          <View className="flex-1 justify-center items-center py-20">
            <Text className="text-6xl mb-4">🌱</Text>
            <Text className="text-xl font-bold text-gray-800 mb-2">Welcome!</Text>
            <Text className="text-gray-600 text-center px-8">
              Start a conversation with your AI farming assistant. Ask about crops, 
              share photos of your fields, or use voice chat for hands-free interaction.
            </Text>
          </View>
        ) : (
          messages.map(renderMessage)
        )}
      </ScrollView>

      {/* Input Area */}
      <View className="bg-white border-t border-gray-200 px-4 py-3">
        {/* Quick Actions */}
        <View className="flex-row justify-center mb-3">
          <TouchableOpacity
            onPress={pickImage}
            className="bg-blue-100 px-4 py-2 rounded-full mr-3"
          >
            <Text className="text-blue-600 font-medium">📷 Gallery</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={takePhoto}
            className="bg-purple-100 px-4 py-2 rounded-full mr-3"
          >
            <Text className="text-purple-600 font-medium">📸 Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={isRecording ? stopRecording : startRecording}
            className={`px-4 py-2 rounded-full ${
              isRecording ? "bg-red-100" : "bg-orange-100"
            }`}
          >
            <Text className={`font-medium ${
              isRecording ? "text-red-600" : "text-orange-600"
            }`}>
              {isRecording ? "⏹️ Stop" : "🎤 Voice"}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Composing Message Preview */}
        {(composingMessage.imageUri || composingMessage.voiceUri) && (
          <View className="bg-gray-100 rounded-lg p-3 mb-3">
            <Text className="text-gray-600 text-sm mb-2">Composing message:</Text>
            {composingMessage.imageUri && (
              <View className="flex-row items-center mb-2">
                <Image
                  source={{ uri: composingMessage.imageUri }}
                  className="w-12 h-12 rounded-lg mr-3"
                  resizeMode="cover"
                />
                <Text className="text-gray-700">📷 Image attached</Text>
              </View>
            )}
            {composingMessage.voiceUri && (
              <View className="flex-row items-center">
                <Text className="text-gray-700">🎤 Voice recording attached</Text>
              </View>
            )}
          </View>
        )}

        {/* Text Input */}
        <View className="flex-row items-center">
          <TextInput
            value={composingMessage.text}
            onChangeText={(text) => setComposingMessage(prev => ({ ...prev, text }))}
            placeholder="Type your message..."
            placeholderTextColor="#9CA3AF"
            className="flex-1 border border-gray-300 rounded-full px-4 py-3 mr-3 bg-gray-50"
            multiline
            maxLength={500}
            onSubmitEditing={handleSend}
            returnKeyType="send"
          />
          <TouchableOpacity
            onPress={handleSend}
            className={`px-6 py-3 rounded-full ${
              composingMessage.text.trim() || composingMessage.imageUri || composingMessage.voiceUri
                ? "bg-green-500" 
                : "bg-gray-300"
            }`}
            disabled={!composingMessage.text.trim() && !composingMessage.imageUri && !composingMessage.voiceUri}
          >
            <Text className="text-white font-bold text-lg">Send</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
