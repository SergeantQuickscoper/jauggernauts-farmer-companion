  import React, { useState } from "react";
  import { View, Text, TextInput, TouchableOpacity, Image, ScrollView, KeyboardAvoidingView, Platform } from "react-native";
  import { LinearGradient } from 'expo-linear-gradient';
  import AsyncStorage from "@react-native-async-storage/async-storage";
  import { router } from "expo-router";

  export default function LoginScreen() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleLogin = async() => {
      setIsLoading(true);
      router.replace("/(tabs)");
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
        setIsLoading(false);
    }

    return(
      <KeyboardAvoidingView 
        className="flex-1 bg-gray-50" 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView className="flex-1" showsVerticalScrollIndicator={false}>
            <View className="items-center">
              <Image
                source={require("../assets/images/icon.png")}
                className="w-80 "
                resizeMode="contain"
              />
              <Text className="text-green-600 text-3xl font-bold text-center mb-2">
                Welcome Back
              </Text>
              <Text className="text-green-600 text-base text-center">
                Your farming companion awaits
              </Text>
            </View>

          <View className="px-6 py-8">
            <View className="bg-white rounded-2xl p-6 shadow-sm">
              <Text className="text-2xl font-bold text-gray-800 mb-6 text-center">
                Sign In
              </Text>
              
              <View className="mb-4">
                <Text className="text-gray-700 font-medium mb-2">Email Address</Text>
                <TextInput
                  placeholder="Enter your email"
                  placeholderTextColor="#9CA3AF"
                  className="w-full border border-gray-200 rounded-xl px-4 py-4 text-gray-800 bg-gray-50"
                  onChangeText={(text) => setEmail(text)}
                  keyboardType="email-address"
                  autoCapitalize="none"
                  autoComplete="email"
                />
              </View>

              <View className="mb-6">
                <Text className="text-gray-700 font-medium mb-2">Password</Text>
                <TextInput
                  placeholder="Enter your password"
                  placeholderTextColor="#9CA3AF"
                  onChangeText={(text) => setPassword(text)}
                  secureTextEntry
                  className="w-full border border-gray-200 rounded-xl px-4 py-4 text-gray-800 bg-gray-50"
                  autoComplete="password"
                />
              </View>

              <TouchableOpacity 
                className={`w-full rounded-xl py-4 mb-6 ${isLoading ? 'bg-gray-400' : 'bg-green-500'}`} 
                onPress={handleLogin}
                disabled={isLoading}
              >
                <Text className="text-white font-bold text-center text-lg">
                  {isLoading ? 'Signing In...' : 'Sign In'}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity className="mb-4">
                <Text className="text-green-600 font-medium text-center">
                  Forgot Password?
                </Text>
              </TouchableOpacity>
            </View>

            <View className="mt-6 bg-white rounded-2xl p-6 shadow-sm">
              <Text className="text-gray-600 text-center mb-4">
                Don&apos;t have an account?
              </Text>
              <TouchableOpacity className="border border-green-500 rounded-xl py-4">
                <Text className="text-green-600 font-bold text-center text-lg">
                  Create Account
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    );
  };
