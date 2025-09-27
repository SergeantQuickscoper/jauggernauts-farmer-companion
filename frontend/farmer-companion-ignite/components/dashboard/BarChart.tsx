import React from 'react';
import { View, Text } from 'react-native';

const chartData = [
  { month: 'Jan', value: 65, color: '#16a34a' },
  { month: 'Feb', value: 78, color: '#22c55e' },
  { month: 'Mar', value: 85, color: '#16a34a' },
  { month: 'Apr', value: 92, color: '#22c55e' },
  { month: 'May', value: 88, color: '#16a34a' },
  { month: 'Jun', value: 95, color: '#22c55e' },
];

const BarChart = ({ data }: { data: typeof chartData }) => {
  const maxValue = Math.max(...data.map(d => d.value));
  
  return (
    <View className="bg-white rounded-xl p-4 mb-4">
      <Text className="text-lg font-bold text-gray-800 mb-4">Crop Yield Trend</Text>
      <View className="flex-row items-end justify-between h-32">
        {data.map((item, index) => (
          <View key={index} className="items-center flex-1">
            <View 
              className="w-6 rounded-t-lg mb-2"
              style={{ 
                height: (item.value / maxValue) * 100,
                backgroundColor: item.color 
              }}
            />
            <Text className="text-xs text-gray-600">{item.month}</Text>
            <Text className="text-xs font-semibold text-gray-800">{item.value}%</Text>
          </View>
        ))}
      </View>
    </View>
  );
};

export default BarChart;