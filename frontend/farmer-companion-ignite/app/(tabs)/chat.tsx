import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  Image,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { LinearGradient } from "expo-linear-gradient";
//import Voice from "@react-native-voice/voice"; 

type Message = {
  id: string;
  sender: "user" | "ai";
  text?: string;
  imageUri?: string;
  createdAt: number;
};

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);

  const addMessage = (msg: Message) => {
    setMessages((prev) => [msg, ...prev]);
  };

  const handleSend = () => {
    if (!input.trim()) return;
    addMessage({
      id: Date.now().toString(),
      sender: "user",
      text: input.trim(),
      createdAt: Date.now(),
    });
    setInput("");
  };

//   // 🎤 Start speech-to-text
//   const startRecording = async () => {
//     setIsRecording(true);
//     Voice.start("en-US");
//     Voice.onSpeechResults = (event) => {
//       if (event.value && event.value.length > 0) {
//         setInput(event.value[0]); // take first recognized phrase
//       }
//     };
//   };

  // 🎤 Stop speech-to-text
//   const stopRecording = async () => {
//     setIsRecording(false);
//     Voice.stop();
//   };

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
    });

    if (!result.canceled) {
      addMessage({
        id: Date.now().toString(),
        sender: "user",
        imageUri: result.assets[0].uri,
        createdAt: Date.now(),
      });
    }
  };

  return (
    <View className="flex-1 bg-white">
      <LinearGradient
              colors={['#16a34a', '#22c55e']}
              className="px-6 py-8"
            >
              <Text className="text-white text-2xl font-bold mb-2 mt-5">Your AI Companion</Text>
              <Text className="text-green-100 text-base">Speak in Malayalam, send pictures or talk about anything.</Text>
      </LinearGradient>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        inverted
        contentContainerStyle={{ padding: 12 }}
        renderItem={({ item }) => (
          <View
            className={`mb-3 max-w-[75%] px-4 py-2 rounded-2xl ${
              item.sender === "user"
                ? "bg-green-500 self-end"
                : "bg-gray-200 self-start"
            }`}
          >
            {item.text && (
              <Text
                className={`${
                  item.sender === "user" ? "text-white" : "text-gray-800"
                }`}
              >
                {item.text}
              </Text>
            )}
            {item.imageUri && (
              <Image
                source={{ uri: item.imageUri }}
                className="w-40 h-40 mt-2 rounded-lg"
              />
            )}
          </View>
        )}
      />
      <View className="flex-row items-center border-t border-gray-200 p-3">
        <TouchableOpacity
          onPress={pickImage}
          className="bg-gray-200 p-3 rounded-full mr-2"
        >
          <Text>🖼️</Text>
        </TouchableOpacity>
        <TouchableOpacity
          //onPress={isRecording ? stopRecording : startRecording}
          className={`p-3 rounded-full mr-2 ${
            isRecording ? "bg-red-500" : "bg-gray-200"
          }`}
        >
          <Text>{isRecording ? "⏹️" : "🎤"}</Text>
        </TouchableOpacity>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder="Type a message..."
          className="flex-1 border border-gray-300 rounded-full px-4 py-2 mr-2"
        />
        <TouchableOpacity
          onPress={handleSend}
          className="bg-green-600 px-4 py-2 rounded-full"
        >
          <Text className="text-white font-bold">Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
