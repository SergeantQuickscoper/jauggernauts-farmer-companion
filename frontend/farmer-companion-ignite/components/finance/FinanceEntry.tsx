import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

export interface FinanceEntryData {
  id: string;
  name: string;
  description: string;
  amount: number;
  type: 'expense' | 'revenue';
  timestamp: Date;
  category: string;
}

interface FinanceEntryProps {
  entry: FinanceEntryData;
  onPress?: () => void;
}

export default function FinanceEntry({ entry, onPress }: FinanceEntryProps) {
  const isExpense = entry.type === 'expense';
  const amountColor = isExpense ? 'text-red-600' : 'text-green-600';
  const amountPrefix = isExpense ? '-' : '+';
  const borderColor = isExpense ? 'border-red-200' : 'border-green-200';
  const bgColor = isExpense ? 'bg-red-50' : 'bg-green-50';

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatAmount = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  return (
    <TouchableOpacity 
      className={`p-4 rounded-xl border-l-4 mb-3 ${borderColor} ${bgColor}`}
      onPress={onPress}
    >
      <View className="flex-row items-start justify-between">
        <View className="flex-1">
          <View className="flex-row items-center mb-1">
            <Text className="font-bold text-gray-800 text-base">{entry.name}</Text>
            <View className={`ml-2 px-2 py-1 rounded-full ${isExpense ? 'bg-red-100' : 'bg-green-100'}`}>
              <Text className={`text-xs font-medium ${isExpense ? 'text-red-700' : 'text-green-700'}`}>
                {entry.category}
              </Text>
            </View>
          </View>
          <Text className="text-gray-600 text-sm mb-2">{entry.description}</Text>
          <Text className="text-gray-500 text-xs">{formatDate(entry.timestamp)}</Text>
        </View>
        <View className="items-end">
          <Text className={`text-lg font-bold ${amountColor}`}>
            {amountPrefix}{formatAmount(entry.amount)}
          </Text>
          <Text className={`text-xs font-medium ${amountColor}`}>
            {entry.type === 'expense' ? 'Expense' : 'Revenue'}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}
