import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Modal, 
  ScrollView,
  Alert 
} from 'react-native';
import { FinanceEntryData } from './FinanceEntry';

interface AddFinanceModalProps {
  visible: boolean;
  onClose: () => void;
  onAdd: (entry: Omit<FinanceEntryData, 'id' | 'timestamp'>) => void;
}

const categories = [
  'Seeds & Fertilizers',
  'Equipment',
  'Labor',
  'Transportation',
  'Utilities',
  'Crop Sales',
  'Livestock Sales',
  'Government Subsidies',
  'Other'
];

export default function AddFinanceModal({ visible, onClose, onAdd }: AddFinanceModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [type, setType] = useState<'expense' | 'revenue'>('expense');
  const [category, setCategory] = useState('');

  const handleSubmit = () => {
    if (!name.trim() || !description.trim() || !amount.trim() || !category.trim()) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    const amountValue = parseFloat(amount);
    if (isNaN(amountValue) || amountValue <= 0) {
      Alert.alert('Error', 'Please enter a valid amount');
      return;
    }

    onAdd({
      name: name.trim(),
      description: description.trim(),
      amount: amountValue,
      type,
      category: category.trim()
    });

    // Reset form
    setName('');
    setDescription('');
    setAmount('');
    setType('expense');
    setCategory('');
    onClose();
  };

  const handleCancel = () => {
    setName('');
    setDescription('');
    setAmount('');
    setType('expense');
    setCategory('');
    onClose();
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View className="flex-1 bg-gray-50">
        <View className="bg-white px-6 py-4 border-b border-gray-200">
          <View className="flex-row items-center justify-between">
            <TouchableOpacity onPress={handleCancel}>
              <Text className="text-green-600 font-medium">Cancel</Text>
            </TouchableOpacity>
            <Text className="text-lg font-bold text-gray-800 text-center justify-center border-2 border-gray-300">Add Finance Entry</Text>
            <TouchableOpacity onPress={handleSubmit}>
              <Text className="text-green-600 font-bold">Save</Text>
            </TouchableOpacity>
          </View>
        </View>

        <ScrollView className="flex-1 px-6 py-4">
          <View className="mb-6">
            <Text className="text-base font-semibold text-gray-800 mb-3">Type</Text>
            <View className="flex-row">
              <TouchableOpacity
                className={`flex-1 py-3 px-4 rounded-xl mr-2 ${
                  type === 'expense' ? 'bg-red-100 border-2 border-red-500' : 'bg-gray-100 border-2 border-gray-300'
                }`}
                onPress={() => setType('expense')}
              >
                <Text className={`text-center font-medium ${
                  type === 'expense' ? 'text-red-700' : 'text-gray-600'
                }`}>
                  Expense
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                className={`flex-1 py-3 px-4 rounded-xl ml-2 ${
                  type === 'revenue' ? 'bg-green-100 border-2 border-green-500' : 'bg-gray-100 border-2 border-gray-300'
                }`}
                onPress={() => setType('revenue')}
              >
                <Text className={`text-center font-medium ${
                  type === 'revenue' ? 'text-green-700' : 'text-gray-600'
                }`}>
                  Revenue
                </Text>
              </TouchableOpacity>
            </View>
          </View>
          <View className="mb-4">
            <Text className="text-base font-semibold text-gray-800 mb-2">Name</Text>
            <TextInput
              value={name}
              onChangeText={setName}
              placeholder="Enter name (e.g., Wheat Sale)"
              className="bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-800"
              placeholderTextColor="#999"
            />
          </View>

          <View className="mb-4">
            <Text className="text-base font-semibold text-gray-800 mb-2">Description</Text>
            <TextInput
              value={description}
              onChangeText={setDescription}
              placeholder="Enter description"
              className="bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-800"
              placeholderTextColor="#999"
              multiline
              numberOfLines={3}
            />
          </View>

          <View className="mb-4">
            <Text className="text-base font-semibold text-gray-800 mb-2">Amount (₹)</Text>
            <TextInput
              value={amount}
              onChangeText={setAmount}
              placeholder="Enter amount"
              className="bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-800"
              placeholderTextColor="#999"
              keyboardType="numeric"
            />
          </View>

          <View className="mb-6">
            <Text className="text-base font-semibold text-gray-800 mb-3">Category</Text>
            <View className="flex-row flex-wrap">
              {categories.map((cat) => (
                <TouchableOpacity
                  key={cat}
                  className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                    category === cat ? 'bg-green-100 border-2 border-green-500' : 'bg-gray-100 border-2 border-gray-300'
                  }`}
                  onPress={() => setCategory(cat)}
                >
                  <Text className={`text-sm font-medium ${
                    category === cat ? 'text-green-700' : 'text-gray-600'
                  }`}>
                    {cat}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
}
