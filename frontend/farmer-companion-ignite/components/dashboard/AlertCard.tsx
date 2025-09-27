import { TouchableOpacity, Text, View } from "react-native";

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

const AlertCard = ({ alert }: { alert: typeof alerts[0] }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-red-500 bg-red-50';
      case 'medium': return 'border-yellow-500 bg-yellow-50';
      case 'low': return 'border-green-500 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  return (
    <TouchableOpacity className={`p-4 rounded-xl border-l-4 mb-3 ${getPriorityColor(alert.priority)}`}>
      <View className="flex-row items-start">
        <Text className="text-2xl mr-3">{alert.icon}</Text>
        <View className="flex-1">
          <Text className="font-bold text-gray-800 text-base">{alert.title}</Text>
          <Text className="text-gray-600 text-sm mt-1">{alert.message}</Text>
          <Text className="text-gray-500 text-xs mt-2">{alert.time}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

export default AlertCard;