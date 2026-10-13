export interface NavItem {
  label: string;
  href: string;
  badge?: string;
}

export interface MoodEdition {
  id: string;
  number: string;
  title: string;
  bengaliTitle: string;
  concept: string;
  paletteDescription: string;
  image: string;
  quote: string;
  accentColor: string;
  ritualId: string;
}

export interface ServiceItem {
  id: string;
  number: string;
  name: string;
  bengaliName?: string;
  category: 'bridal' | 'skincare' | 'hair' | 'nails' | 'men';
  categoryLabel: string;
  duration: string;
  price: number;
  formattedPrice: string;
  description: string;
  botanicalNotes: string[];
  isSignature?: boolean;
  image: string;
}

export interface Stylist {
  id: string;
  name: string;
  role: string;
  experience: string;
  speciality: string;
  credentials: string[];
  philosophy: string;
  image: string;
  rating: number;
}

export interface TransformationItem {
  id: string;
  title: string;
  category: string;
  imageBefore: string;
  imageAfter: string;
  notes: string;
}

export interface SensoryNote {
  dimension: string;
  element: string;
  origin: string;
  description: string;
}

export interface SalonSuite {
  id: string;
  number: string;
  name: string;
  bengaliName: string;
  subtitle: string;
  image: string;
  atmosphere: string;
  hotspots: string[];
}

export interface LookbookPhoto {
  id: string;
  title: string;
  category: 'Bridal Makeup' | 'Skin Glow' | 'Hair Art' | 'Nail Care' | 'Salon Suites';
  image: string;
  caption: string;
}

export interface CalculatorItem {
  id: string;
  name: string;
  category: string;
  durationMinutes: number;
  duration: string;
  price: number;
  formattedPrice: string;
}

export interface BookingFormData {
  serviceId: string;
  stylistId: string;
  date: string;
  timeSlot: string;
  clientName: string;
  clientEmail: string;
  clientPhone: string;
  notes: string;
}
