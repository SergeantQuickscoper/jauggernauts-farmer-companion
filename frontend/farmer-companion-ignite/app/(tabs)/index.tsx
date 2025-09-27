import React from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AlertCard from '@/components/dashboard/AlertCard';


// TODO: add a crop price watchlist

// vibe data
const alerts = [
  {
    id: 1,
    title: 'Water Level Low',
    message: 'Field A irrigation system needs attention',
    time: '2 hours ago',
    priority: 'high',
    icon: '💧'
  },
  {
    id: 2,
    title: 'Harvest Ready',
    message: 'Wheat crop in Field B is ready for harvest',
    time: '1 day ago',
    priority: 'medium',
    icon: '🌾'
  },
  {
    id: 3,
    title: 'Weather Alert',
    message: 'Heavy rain expected in next 24 hours',
    time: '3 hours ago',
    priority: 'high',
    icon: '⛈️'
  },
  {
    id: 4,
    title: 'Equipment Maintenance',
    message: 'Tractor service due next week',
    time: '2 days ago',
    priority: 'low',
    icon: '🚜'
  }
];

export default function HomeScreen() {
  return (
    <ScrollView className="flex-1 bg-gray-50">
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <Text className="text-white text-2xl font-bold mb-2 mt-5">Dashboard</Text>
        <Text className="text-green-100 text-base">Welcome back! Here&apos;s your farm overview</Text>
      </LinearGradient>

      <View className="px-6">
        <View className="bg-white rounded-xl p-4">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-lg font-bold text-gray-800">Important Farm Alerts</Text>
            <TouchableOpacity className="bg-green-100 px-3 py-1 rounded-full">
              <Text className="text-green-700 text-sm font-medium">View All</Text>
            </TouchableOpacity>
          </View>
          
          {alerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))}
        </View>
      </View>

      <View className="h-6" />
    </ScrollView>
  );
}
