'use client';

import React, { createContext, useContext, useState } from 'react';
import { ServiceItem } from '@/types';

interface BookingContextType {
  isBookingOpen: boolean;
  selectedService: ServiceItem | null;
  openBooking: (service?: ServiceItem | null) => void;
  closeBooking: () => void;
  selectedArticleId: string | null;
  openArticleModal: (id: string) => void;
  closeArticleModal: () => void;
}

const BookingContext = createContext<BookingContextType | undefined>(undefined);

export function BookingProvider({ children }: { children: React.ReactNode }) {
  const [isBookingOpen, setIsBookingOpen] = useState(false);
  const [selectedService, setSelectedService] = useState<ServiceItem | null>(null);
  const [selectedArticleId, setSelectedArticleId] = useState<string | null>(null);

  const openBooking = (service?: ServiceItem | null) => {
    if (service) {
      setSelectedService(service);
    }
    setIsBookingOpen(true);
  };

  const closeBooking = () => {
    setIsBookingOpen(false);
  };

  const openArticleModal = (id: string) => {
    setSelectedArticleId(id);
  };

  const closeArticleModal = () => {
    setSelectedArticleId(null);
  };

  return (
    <BookingContext.Provider
      value={{
        isBookingOpen,
        selectedService,
        openBooking,
        closeBooking,
        selectedArticleId,
        openArticleModal,
        closeArticleModal,
      }}
    >
      {children}
    </BookingContext.Provider>
  );
}

export function useBooking() {
  const context = useContext(BookingContext);
  if (!context) {
    throw new Error('useBooking must be used within a BookingProvider');
  }
  return context;
}
