import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';

export default function Settings() {
  const handleBackToIndex = () => {
    router.replace('/login');
  };

  return (
    <ScrollView className="flex-1 bg-gray-50">
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <Text className="text-white text-2xl font-bold mb-2 mt-5">Settings</Text>
        <Text className="text-green-100 text-base">Manage your app preferences</Text>
      </LinearGradient>

      <View className="px-6 py-6">
        <View className="bg-white rounded-xl p-6">
          <Text className="text-lg font-bold text-gray-800 mb-4">Settings</Text>
          
          <TouchableOpacity 
            onPress={handleBackToIndex}
            className="bg-green-500 px-6 py-3 rounded-lg mb-4"
          >
            <Text className="text-white text-center font-medium">Logout</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}