import React, { useState } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import FinanceEntry, { FinanceEntryData } from '@/components/finance/FinanceEntry';
import FinanceChart from '@/components/finance/FinanceChart';
import AddFinanceModal from '@/components/finance/AddFinanceModal';

// more vibe data
const initialFinanceEntries: FinanceEntryData[] = [
  {
    id: '1',
    name: 'Wheat Harvest Sale',
    description: 'Sold 500kg of wheat to local market',
    amount: 25000,
    type: 'revenue',
    timestamp: new Date('2024-01-15T10:30:00'),
    category: 'Crop Sales'
  },
  {
    id: '2',
    name: 'Fertilizer Purchase',
    description: 'Bought NPK fertilizer for rice field',
    amount: 8500,
    type: 'expense',
    timestamp: new Date('2024-01-14T14:20:00'),
    category: 'Seeds & Fertilizers'
  },
  {
    id: '3',
    name: 'Tractor Fuel',
    description: 'Diesel for field preparation',
    amount: 3200,
    type: 'expense',
    timestamp: new Date('2024-01-13T09:15:00'),
    category: 'Transportation'
  },
  {
    id: '4',
    name: 'Government Subsidy',
    description: 'PM-KISAN scheme payment received',
    amount: 6000,
    type: 'revenue',
    timestamp: new Date('2024-01-12T16:45:00'),
    category: 'Government Subsidies'
  },
  {
    id: '5',
    name: 'Labor Wages',
    description: 'Daily wages for field workers',
    amount: 4500,
    type: 'expense',
    timestamp: new Date('2024-01-11T18:00:00'),
    category: 'Labor'
  },
  {
    id: '6',
    name: 'Rice Sale',
    description: 'Sold 300kg of basmati rice',
    amount: 18000,
    type: 'revenue',
    timestamp: new Date('2024-01-10T11:30:00'),
    category: 'Crop Sales'
  }
];

export default function Finance() {
  const [entries, setEntries] = useState<FinanceEntryData[]>(initialFinanceEntries);
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterType, setFilterType] = useState<'all' | 'expense' | 'revenue'>('all');

  const addEntry = (entryData: Omit<FinanceEntryData, 'id' | 'timestamp'>) => {
    const newEntry: FinanceEntryData = {
      ...entryData,
      id: Date.now().toString(),
      timestamp: new Date()
    };
    setEntries(prev => [newEntry, ...prev]);
  };

  const filteredEntries = entries.filter(entry => {
    if (filterType === 'all') return true;
    return entry.type === filterType;
  });

  const totalRevenue = entries
    .filter(entry => entry.type === 'revenue')
    .reduce((sum, entry) => sum + entry.amount, 0);
  
  const totalExpenses = entries
    .filter(entry => entry.type === 'expense')
    .reduce((sum, entry) => sum + entry.amount, 0);

  return (
    <View className="flex-1 bg-gray-50">
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <Text className="text-white text-2xl font-bold mb-2 mt-5">Finance Tracker</Text>
        <Text className="text-green-100 text-base">Track your farm expenses and revenue</Text>
      </LinearGradient>
      {/* TODO: Add a ScrollView */}
      <ScrollView className="flex-1">
      <View className="px-6 py-4">
        <View className="flex-row mb-4">
          <View className="flex-1 bg-green-50 rounded-xl p-4 mr-2">
            <Text className="text-green-600 text-sm font-medium mb-1">Total Revenue</Text>
            <Text className="text-green-700 text-xl font-bold">₹{totalRevenue.toLocaleString()}</Text>
          </View>
          <View className="flex-1 bg-red-50 rounded-xl p-4 ml-2">
            <Text className="text-red-600 text-sm font-medium mb-1">Total Expenses</Text>
            <Text className="text-red-700 text-xl font-bold">₹{totalExpenses.toLocaleString()}</Text>
          </View>
        </View>
      </View>

      <View className="px-6">
        <FinanceChart entries={entries} />
      </View>

      <View className="px-6 mb-4">
        <View className="flex-row bg-white rounded-xl p-1">
          <TouchableOpacity
            className={`flex-1 py-2 px-4 rounded-lg ${
              filterType === 'all' ? 'bg-green-600' : 'bg-transparent'
            }`}
            onPress={() => setFilterType('all')}
          >
            <Text className={`text-center font-medium ${
              filterType === 'all' ? 'text-white' : 'text-gray-600'
            }`}>
              All
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 px-4 rounded-lg ${
              filterType === 'revenue' ? 'bg-green-600' : 'bg-transparent'
            }`}
            onPress={() => setFilterType('revenue')}
          >
            <Text className={`text-center font-medium ${
              filterType === 'revenue' ? 'text-white' : 'text-gray-600'
            }`}>
              Revenue
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className={`flex-1 py-2 px-4 rounded-lg ${
              filterType === 'expense' ? 'bg-green-600' : 'bg-transparent'
            }`}
            onPress={() => setFilterType('expense')}
          >
            <Text className={`text-center font-medium ${
              filterType === 'expense' ? 'text-white' : 'text-gray-600'
            }`}>
              Expenses
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View className="px-6 flex-1">
        <View className="bg-white rounded-xl p-4 flex-1">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-lg font-bold text-gray-800">
              {filterType === 'all' ? 'All Transactions' : 
               filterType === 'revenue' ? 'Revenue' : 'Expenses'}
            </Text>
            <TouchableOpacity 
              className="bg-green-600 px-4 py-2 rounded-full"
              onPress={() => setShowAddModal(true)}
            >
              <Text className="text-white font-bold text-sm">+ Add Entry</Text>
            </TouchableOpacity>
          </View>
          
          {filteredEntries.length > 0 ? (
            filteredEntries.map((item) => (
              <FinanceEntry 
                key={item.id}
                entry={item} 
                onPress={() => {
                  // Could add edit functionality here
                }}
              />
            ))
          ) : (
            <View className="py-8 items-center">
              <Text className="text-gray-500 text-center">
                No {filterType === 'all' ? 'transactions' : filterType} found
              </Text>
              <Text className="text-gray-400 text-sm mt-2">
                Tap &quot;+ Add Entry&quot; to get started
              </Text>
            </View>
          )}
        </View>
      </View>
      </ScrollView>

      <AddFinanceModal
        visible={showAddModal}
        onClose={() => setShowAddModal(false)}
        onAdd={addEntry}
      />
    </View>
  );
}