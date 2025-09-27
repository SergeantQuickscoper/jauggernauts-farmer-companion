import React from 'react';
import { View, Text } from 'react-native';
import { FinanceEntryData } from './FinanceEntry';

interface FinanceChartProps {
  entries: FinanceEntryData[];
}

export default function FinanceChart({ entries }: FinanceChartProps) {
  const totalRevenue = entries
    .filter(entry => entry.type === 'revenue')
    .reduce((sum, entry) => sum + entry.amount, 0);
  
  const totalExpenses = entries
    .filter(entry => entry.type === 'expense')
    .reduce((sum, entry) => sum + entry.amount, 0);
  
  const netProfit = totalRevenue - totalExpenses;
  

  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - i);
    return date;
  }).reverse();

  const dailyData = last7Days.map(date => {
    const dayEntries = entries.filter(entry => {
      const entryDate = new Date(entry.timestamp);
      return entryDate.toDateString() === date.toDateString();
    });
    
    const dayRevenue = dayEntries
      .filter(entry => entry.type === 'revenue')
      .reduce((sum, entry) => sum + entry.amount, 0);
    
    const dayExpenses = dayEntries
      .filter(entry => entry.type === 'expense')
      .reduce((sum, entry) => sum + entry.amount, 0);
    
    return {
      date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      revenue: dayRevenue,
      expenses: dayExpenses,
      net: dayRevenue - dayExpenses
    };
  });

  const maxAmount = Math.max(
    ...dailyData.map(d => Math.max(d.revenue, d.expenses))
  );

  const formatAmount = (amount: number) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    } else if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    }
    return `₹${amount}`;
  };

  return (
    <View className="bg-white rounded-xl p-4 mb-4">
      <Text className="text-lg font-bold text-gray-800 mb-4">Financial Overview</Text>
      
      <View className="flex-row mb-4">
        <View className="flex-1 bg-green-50 rounded-lg p-3 mr-2">
          <Text className="text-green-600 text-xs font-medium mb-1">Total Revenue</Text>
          <Text className="text-green-700 text-lg font-bold">{formatAmount(totalRevenue)}</Text>
        </View>
        <View className="flex-1 bg-red-50 rounded-lg p-3 ml-2">
          <Text className="text-red-600 text-xs font-medium mb-1">Total Expenses</Text>
          <Text className="text-red-700 text-lg font-bold">{formatAmount(totalExpenses)}</Text>
        </View>
      </View>
      
        <View className={`rounded-lg p-3 mb-4 ${netProfit >= 0 ? 'bg-green-50' : 'bg-red-50'}`}>
        <Text className={`text-xs font-medium mb-1 ${netProfit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          Net Profit
        </Text>
        <Text className={`text-xl font-bold ${netProfit >= 0 ? 'text-green-700' : 'text-red-700'}`}>
          {netProfit >= 0 ? '+' : ''}{formatAmount(netProfit)}
        </Text>
      </View>

      <View>
        <Text className="text-sm font-semibold text-gray-700 mb-3">Last 7 Days Trend</Text>
        <View className="flex-row items-end justify-between h-20">
          {dailyData.map((day, index) => (
            <View key={index} className="items-center flex-1">
              <View className="flex-col items-center mb-1">

                <View 
                  className="w-3 bg-green-500 rounded-t-sm mb-0.5"
                  style={{ 
                    height: maxAmount > 0 ? (day.revenue / maxAmount) * 40 : 0
                  }}
                />

                <View 
                  className="w-3 bg-red-500 rounded-b-sm"
                  style={{ 
                    height: maxAmount > 0 ? (day.expenses / maxAmount) * 40 : 0
                  }}
                />
              </View>
              <Text className="text-xs text-gray-600">{day.date}</Text>
            </View>
          ))}
        </View>
        
        <View className="flex-row justify-center mt-3">
          <View className="flex-row items-center mr-4">
            <View className="w-3 h-3 bg-green-500 rounded-sm mr-2" />
            <Text className="text-xs text-gray-600">Revenue</Text>
          </View>
          <View className="flex-row items-center">
            <View className="w-3 h-3 bg-red-500 rounded-sm mr-2" />
            <Text className="text-xs text-gray-600">Expenses</Text>
          </View>
        </View>
      </View>
    </View>
  );
}
