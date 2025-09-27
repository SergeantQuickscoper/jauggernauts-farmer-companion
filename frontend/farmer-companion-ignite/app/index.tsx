import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, Image } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router, Router } from "expo-router";
export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const handleLogin = async() => {
    router.push("/(tabs)");
    const em = email
    const pass = password
    try {
        await fetch(process.env.BACKEND_URL + "user/login", {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: em,
        password: pass
       }),
    })
    .then((response) => console.log(response.json()))
      } catch (error) {
        console.log(error);
        return;
      }
      await AsyncStorage.setItem("userEmail", em);
      await AsyncStorage.setItem("userPassword", pass);
      
  }
  return(
    <View className="flex-1 bg-white px-6">
      <View className="items-center">
        <Image
          source={require("../assets/images/icon.png")}
          className="w-96 h-96"
          resizeMode="contain"
        />
        <Text className="text-2xl font-bold text-gray-800 text-center mb-10">Welcome to the one stop solution for all your farming needs</Text>
      </View>
      <TextInput
        placeholder="Email"
        placeholderTextColor="#999"
        className="w-full border border-gray-300 rounded-xl px-4 py-3 mb-4 text-gray-800"
        onChangeText={(text) => setEmail(text)}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Password"
        placeholderTextColor="#999"
        onChangeText={(text) => setPassword(text)}
        secureTextEntry
        className="w-full border border-gray-300 rounded-xl px-4 py-3 mb-6 text-gray-800"
      />
      <TouchableOpacity className="w-full bg-green-600 rounded-xl py-3 mb-4" onPress={handleLogin}>
        <Text className="text-white font-bold text-center text-lg">Login</Text>
      </TouchableOpacity>

      <View className="flex-row justify-between w-full">
        <TouchableOpacity>
          <Text className="text-green-600 font-medium">Forgot Password?</Text>
        </TouchableOpacity>
        <TouchableOpacity>
          <Text className="text-green-600 font-medium">Don&apos;t have an Account? Sign up!</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
  };
