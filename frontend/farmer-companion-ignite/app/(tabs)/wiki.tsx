import React, { useState } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity,
  Image,
  TextInput 
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface CropGuide {
  id: string;
  name: string;
  emoji: string;
  season: string;
  duration: string;
  description: string;
  steps: string[];
  tips: string[];
  requirements: {
    soil: string;
    water: string;
    temperature: string;
    spacing: string;
  };
}

const cropGuides: CropGuide[] = [
  {
    id: '1',
    name: 'Rice (Paddy)',
    emoji: '🌾',
    season: 'Kharif (June-October)',
    duration: '120-150 days',
    description: 'The staple crop of Kerala, grown in both Kharif and Rabi seasons',
    steps: [
      'Prepare the field with proper leveling and bunding',
      'Soak seeds for 12-24 hours before sowing',
      'Transplant seedlings when they are 25-30 days old',
      'Maintain 2-3 cm water level during growth',
      'Apply fertilizers in 3 splits: basal, tillering, and panicle initiation',
      'Control weeds and pests regularly',
      'Harvest when 80% of grains are mature'
    ],
    tips: [
      'Use certified seeds for better yield',
      'Practice crop rotation to maintain soil health',
      'Monitor water levels carefully during flowering',
      'Use organic fertilizers for sustainable farming'
    ],
    requirements: {
      soil: 'Clay loam with good water retention',
      water: 'Continuous flooding or alternate wetting and drying',
      temperature: '25-35°C',
      spacing: '20x15 cm between plants'
    }
  },
  {
    id: '2',
    name: 'Coconut',
    emoji: '🥥',
    season: 'Year-round',
    duration: '6-8 years to first harvest',
    description: 'The tree of life in Kerala, providing multiple products',
    steps: [
      'Select healthy seedlings from certified nurseries',
      'Prepare pits of 1x1x1 meter size',
      'Plant during monsoon season (June-August)',
      'Apply organic manure and fertilizers regularly',
      'Provide adequate irrigation during dry periods',
      'Control pests like rhinoceros beetle and red palm weevil',
      'Harvest mature nuts every 45-60 days'
    ],
    tips: [
      'Plant windbreaks to protect young palms',
      'Use integrated pest management',
      'Practice intercropping with banana or vegetables',
      'Maintain proper drainage to prevent waterlogging'
    ],
    requirements: {
      soil: 'Well-drained sandy loam to clay loam',
      water: 'Regular irrigation, 100-150 liters per tree',
      temperature: '20-30°C',
      spacing: '7.5x7.5 meters between trees'
    }
  },
  {
    id: '3',
    name: 'Banana',
    emoji: '🍌',
    season: 'Year-round',
    duration: '12-15 months',
    description: 'High-value crop with good market demand',
    steps: [
      'Select healthy suckers from disease-free plants',
      'Prepare pits of 60x60x60 cm',
      'Plant during monsoon season',
      'Apply organic manure and fertilizers',
      'Provide support with bamboo poles',
      'Remove excess suckers, keep only 2-3 per plant',
      'Harvest when fingers are fully developed'
    ],
    tips: [
      'Use tissue culture plants for uniform growth',
      'Practice mulching to retain moisture',
      'Control bunchy top virus through clean planting material',
      'Harvest in early morning for better quality'
    ],
    requirements: {
      soil: 'Well-drained fertile soil',
      water: 'Regular irrigation, avoid waterlogging',
      temperature: '25-35°C',
      spacing: '2x2 meters between plants'
    }
  },
  {
    id: '4',
    name: 'Spices (Black Pepper)',
    emoji: '🌶️',
    season: 'Year-round',
    duration: '3-4 years to first harvest',
    description: 'Kerala is famous for its high-quality spices',
    steps: [
      'Select healthy cuttings from high-yielding vines',
      'Prepare support system with live standards',
      'Plant during monsoon season',
      'Provide adequate shade and support',
      'Apply organic fertilizers and compost',
      'Control pests and diseases regularly',
      'Harvest when berries turn red'
    ],
    tips: [
      'Use live standards like silver oak or coconut',
      'Maintain proper shade (50-60%)',
      'Practice organic farming for premium prices',
      'Harvest at right maturity for best quality'
    ],
    requirements: {
      soil: 'Well-drained laterite soil',
      water: 'Regular irrigation during dry periods',
      temperature: '20-30°C',
      spacing: '3x3 meters between standards'
    }
  },
  {
    id: '5',
    name: 'Vegetables (Okra)',
    emoji: '🥒',
    season: 'Year-round',
    duration: '45-60 days',
    description: 'Quick-growing vegetable with good market value',
    steps: [
      'Prepare raised beds for better drainage',
      'Sow seeds directly or use seedlings',
      'Maintain proper spacing between plants',
      'Apply balanced fertilizers',
      'Provide regular irrigation',
      'Control pests like fruit borer and aphids',
      'Harvest tender pods every 2-3 days'
    ],
    tips: [
      'Use resistant varieties for pest control',
      'Practice crop rotation to prevent diseases',
      'Harvest in early morning for better quality',
      'Remove old pods to encourage new growth'
    ],
    requirements: {
      soil: 'Well-drained fertile soil',
      water: 'Regular irrigation, avoid waterlogging',
      temperature: '25-35°C',
      spacing: '30x15 cm between plants'
    }
  }
];

export default function Wiki() {
  const [selectedCrop, setSelectedCrop] = useState<CropGuide | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredCrops = cropGuides.filter(crop =>
    crop.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    crop.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    crop.season.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderCropCard = (crop: CropGuide) => (
    <TouchableOpacity
      key={crop.id}
      className="bg-white rounded-xl p-4 mb-4 shadow-sm"
      onPress={() => setSelectedCrop(crop)}
    >
      <View className="flex-row items-center">
        <Text className="text-3xl mr-4">{crop.emoji}</Text>
        <View className="flex-1">
          <Text className="text-lg font-bold text-gray-800">{crop.name}</Text>
          <Text className="text-sm text-gray-600">{crop.season}</Text>
          <Text className="text-sm text-gray-500">{crop.duration}</Text>
        </View>
        <Text className="text-gray-400">›</Text>
      </View>
    </TouchableOpacity>
  );

  const renderCropDetail = (crop: CropGuide) => (
    <ScrollView className="flex-1 bg-gray-50">
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <TouchableOpacity 
          className="mb-4"
          onPress={() => setSelectedCrop(null)}
        >
          <Text className="text-white text-lg mt-6">‹ Back to Crops</Text>
        </TouchableOpacity>
        <View className="items-center">
          <Text className="text-6xl mb-4">{crop.emoji}</Text>
          <Text className="text-white text-2xl font-bold text-center mb-2">
            {crop.name}
          </Text>
          <Text className="text-green-100 text-base text-center">
            {crop.description}
          </Text>
        </View>
      </LinearGradient>

      <View className="px-6 py-6">
        {/* Basic Info */}
        <View className="bg-white rounded-xl p-4 mb-4">
          <Text className="text-lg font-bold text-gray-800 mb-3">Basic Information</Text>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Season:</Text>
            <Text className="text-gray-800 font-medium">{crop.season}</Text>
          </View>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Duration:</Text>
            <Text className="text-gray-800 font-medium">{crop.duration}</Text>
          </View>
        </View>

        {/* Growing Steps */}
        <View className="bg-white rounded-xl p-4 mb-4">
          <Text className="text-lg font-bold text-gray-800 mb-3">Growing Steps</Text>
          {crop.steps.map((step, index) => (
            <View key={index} className="flex-row mb-2">
              <Text className="text-green-600 font-bold mr-3">{index + 1}.</Text>
              <Text className="text-gray-700 flex-1">{step}</Text>
            </View>
          ))}
        </View>

        {/* Requirements */}
        <View className="bg-white rounded-xl p-4 mb-4">
          <Text className="text-lg font-bold text-gray-800 mb-3">Requirements</Text>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Soil:</Text>
            <Text className="text-gray-800 font-medium text-right flex-1 ml-4">{crop.requirements.soil}</Text>
          </View>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Water:</Text>
            <Text className="text-gray-800 font-medium text-right flex-1 ml-4">{crop.requirements.water}</Text>
          </View>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Temperature:</Text>
            <Text className="text-gray-800 font-medium text-right flex-1 ml-4">{crop.requirements.temperature}</Text>
          </View>
          <View className="flex-row justify-between mb-2">
            <Text className="text-gray-600">Spacing:</Text>
            <Text className="text-gray-800 font-medium text-right flex-1 ml-4">{crop.requirements.spacing}</Text>
          </View>
        </View>

        {/* Tips */}
        <View className="bg-white rounded-xl p-4 mb-6">
          <Text className="text-lg font-bold text-gray-800 mb-3">Pro Tips</Text>
          {crop.tips.map((tip, index) => (
            <View key={index} className="flex-row mb-2">
              <Text className="text-green-600 font-bold mr-3">💡</Text>
              <Text className="text-gray-700 flex-1">{tip}</Text>
            </View>
          ))}
        </View>
      </View>
    </ScrollView>
  );

  if (selectedCrop) {
    return renderCropDetail(selectedCrop);
  }

  return (
    <ScrollView className="flex-1 bg-gray-50">
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="px-6 py-8"
      >
        <Text className="text-white text-2xl font-bold mb-2 mt-5">Crop Guide</Text>
        <Text className="text-green-100 text-base">Learn to grow crops in Kerala</Text>
      </LinearGradient>

      <View className="px-6 py-6">
        <View className="bg-white rounded-xl p-4 mb-6">
          <Text className="text-lg font-bold text-gray-800 mb-2">Welcome to the Kerala Farming Guide</Text>
          <Text className="text-gray-600 text-sm">
            Discover the best practices for growing crops in Kerala&apos;s unique climate and soil conditions. 
            Each guide includes step-by-step instructions, requirements, and expert tips, and the list gets updated regularly.
          </Text>
        </View>

        <Text className="text-lg font-bold text-gray-800 mb-4">Popular Crops in Kerala</Text>
        
        {/* Search Bar */}
        <View className="bg-white rounded-xl p-4 mb-4 shadow-sm">
          <TextInput
            placeholder="Search crops, seasons, or descriptions..."
            placeholderTextColor="#9CA3AF"
            className="w-full border border-gray-200 rounded-lg px-4 py-3 text-gray-800 bg-gray-50"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {filteredCrops.length > 0 ? (
          filteredCrops.map(renderCropCard)
        ) : (
          <View className="bg-white rounded-xl p-6 items-center">
            <Text className="text-gray-500 text-center text-lg mb-2">
              No crops found
            </Text>
            <Text className="text-gray-400 text-center text-sm">
              Try searching for "rice", "coconut", "banana", "spices", or "vegetables"
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}