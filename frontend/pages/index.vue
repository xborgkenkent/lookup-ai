<template>
    <div class="max-w-2xl mx-auto p-4 w-full">
      <div class="bg-white rounded-xl shadow-md p-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-6">Lookup.ai</h1>
  
        <form @submit.prevent="handleSubmit" class="mb-6">
          <div class="relative mb-4">
            <label for="search" class="block text-sm font-medium text-gray-700 mb-2">
              Search Anything
            </label>
            <div class="relative">
              <input
                  id="search"
                  type="text"
                  v-model="search"
                  placeholder="Find me a cheap sushi restaurant in downtown Los Angeles..."
                  class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-gray-700"
                  required
              />
              <Search class="absolute left-3 top-3.5 text-gray-400" :size="20" />
            </div>
            <p class="mt-2 text-xs text-gray-500">
              Try: "Find me a cheap sushi restaurant in downtown Los Angeles that's open now and has at least a 4-star rating."
            </p>
          </div>
  
          <!-- Filter selection -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Filter By
            </label>
            <div class="flex gap-2">
              <button
                  type="button"
                  @click="filterType = 'restaurant'"
                  class="flex-1 py-2 px-4 rounded-lg border transition-all"
                  :class="filterType === 'restaurant' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <div class="flex items-center justify-center gap-2">
                  <Utensils class="h-4 w-4" />
                  Restaurant
                </div>
              </button>
              <button
                  type="button"
                  @click="filterType = 'hotel'"
                  class="flex-1 py-2 px-4 rounded-lg border transition-all"
                  :class="filterType === 'hotel' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <div class="flex items-center justify-center gap-2">
                  <Hotel class="h-4 w-4" />
                  Hotel
                </div>
              </button>
            </div>
          </div>
  
          <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 flex items-center justify-center disabled:opacity-70"
          >
            <template v-if="isLoading">
              <Loader2 class="animate-spin mr-2" :size="20" />
              Searching...
            </template>
            <template v-else>
              <Search class="mr-2" :size="20" />
              Lookup
            </template>
          </button>
        </form>
  
        <div v-for="place in filteredResults" :key="place.fsq_id" class="mb-6 border-b pb-4 last:border-0">
          <div class="relative flex flex-col">
            <div class="flex items-center gap-2">
              <div v-if="place.type === 'restaurant'" class="p-1 bg-orange-100 rounded-md">
                <Utensils class="h-4 w-4 text-orange-500" />
              </div>
              <div v-else-if="place.type === 'hotel'" class="p-1 bg-blue-100 rounded-md">
                <Hotel class="h-4 w-4 text-blue-500" />
              </div>
              <p class="text-lg font-bold text-gray-800">{{ place.name }}</p>
            </div>
            <div class="flex items-center gap-2 mt-2" v-if="place.address">
              <MapPinHouse class="h-5 w-5 text-gray-500" />
              <p class="text-sm text-gray-700">{{ place.address }}</p>
            </div>
            <div class="flex flex-col mt-2" v-if="place.hours">
              <div class="flex items-center gap-2">
                <CalendarClock class="h-5 w-5 text-gray-500" />
                <p class="text-sm font-medium text-gray-700">Hours:</p>
              </div>
              <div class="ml-7">
                <div v-for="(schedule, index) in formatSchedule(place.hours)" :key="index" class="text-sm text-gray-600">
                  {{ schedule }}
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2 mt-2" v-if="place.price">
              <DollarSign class="h-5 w-5 text-gray-500" />
              <p class="text-sm text-gray-700">{{ place.price }}</p>
            </div>
            <div class="flex items-center gap-2 mt-2" v-if="place.rating">
              <Star class="h-5 w-5 text-yellow-500" />
              <p class="text-sm text-gray-700">{{ place.rating.toFixed(1) }}</p>
            </div>
            <div class="flex items-center gap-2 mt-2" v-if="place.cuisine && filterType === 'restaurant'">
              <Hamburger class="h-5 w-5 text-gray-500" />
              <a :href=place.cuisine class="text-sm text-blue-300">{{ place.cuisine }}</a>
            </div>
            <div class="flex items-center gap-2 mt-2" v-if="place.features?.amenities && filterType === 'hotel'">
              <Star class="h-5 w-5 text-yellow-500" />
              <p class="text-sm text-gray-700">{{ formatAmenities(place.features?.amenities) }}</p>
            </div>
          </div>
        </div>
  
        <div v-if="error" class="mt-4 p-4 bg-red-50 text-red-800 rounded-lg">
          {{ error }}
        </div>
  
        <div v-if="!isLoading && filteredResults.length === 0 && !error" class="mt-4 p-4 bg-gray-50 text-gray-600 rounded-lg text-center">
          <template v-if="results.length > 0">
            No results match the selected filter. Try changing your filter.
          </template>
          <template v-else>
            Search to see results here.
          </template>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang='ts'>
  import { Search, MapPinHouse, CalendarClock, DollarSign, Star, Hamburger, Loader2, Utensils, Hotel } from 'lucide-vue-next'
  
  interface Place {
    name: string
    rating?: number
    price?: number
    hours?: string
    address?: string
    cuisine?: string
    fsq_id?: string
    features?: Features
    type: 'restaurant' | 'hotel'
  }
  
  interface Features {
    amenities?: Amenities
  }
  
  interface Amenities {
    restroom?: boolean
    smoking?: boolean
    jukebox?: boolean
    music?: boolean
    live_music?: boolean
    private_room?: boolean
    outdoor_seating?: boolean
    tvs?: boolean
    atm?: boolean
    coat_check?: boolean
    wheelchair_accessible?: boolean
    parking?: boolean
    sit_down_dining?: boolean
    wifi?: boolean
  }
  const config = useRuntimeConfig()
  const search = ref('')
  const results = ref<Place[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const filterType = ref<'restaurant' | 'hotel' | null>(null)
  
  const filteredResults = computed(() => {
    if (!filterType.value) return results.value
    return results.value.filter(place => {
      return place.type === filterType.value
    })
  })
  
  const formatSchedule = (hours: string): string[] => {
    if (!hours) return []
  
    return hours.split(';').map(schedule => {
      return schedule.trim()
    })
  }
  
  const formatAmenities = (amenities: Amenities): string => {
    if (!amenities) return ''
  
    const enabledAmenities = Object.entries(amenities)
        .filter(([_, value]) => value === true)
        .map(([key]) => key.replace(/_/g, ' '))
        .map(amenity => amenity.charAt(0).toUpperCase() + amenity.slice(1))
  
    return enabledAmenities.join(', ')
  }
  
  const handleSubmit = async () => {
    if (!search.value.trim()) return
  
    isLoading.value = true
    error.value = null
  
    try {
      const response = await fetch(`${config.public.baseUrl}/api/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"message": search.value, "action": filterType.value}),
        credentials: 'include',
      })
  
      if (!response.ok) {
        throw new Error('Failed to fetch results')
      }
      const data = await response.json()
      results.value.push(...data)
  
    } catch (err) {
      console.error(err)
      error.value = 'Try again...'
    } finally {
      isLoading.value = false
    }
  }
  </script>