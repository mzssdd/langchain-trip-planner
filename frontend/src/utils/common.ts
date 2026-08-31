import dayjs, { type Dayjs } from 'dayjs'

import type { PartyInfo } from '@/types'

export const TRIP_PLAN_STORAGE_KEY = 'tripPlan'

export function getTravelDays(startDate: Dayjs | null, endDate: Dayjs | null): number {
  if (!startDate || !endDate) {
    return 1
  }

  return endDate.diff(startDate, 'day') + 1
}

export function getPartyTotal(party: Pick<PartyInfo, 'adults' | 'children' | 'elders'>): number {
  return Number(party.adults || 0) + Number(party.children || 0) + Number(party.elders || 0)
}

export function getDefaultCompanionType(
  party: Pick<PartyInfo, 'adults' | 'children' | 'elders'>
): PartyInfo['companion_type'] {
  const total = getPartyTotal(party)

  if (party.children > 0) {
    return 'family_with_children'
  }

  if (party.elders > 0) {
    return 'family_with_elders'
  }

  if (total <= 1) {
    return 'solo'
  }

  if (total === 2) {
    return 'couple'
  }

  if (total > 2) {
    return 'friends'
  }

  return 'other'
}

export function formatDateValue(dateValue: Dayjs | string | null): string {
  if (!dateValue) {
    return ''
  }

  if (typeof dateValue === 'string') {
    return dayjs(dateValue).format('YYYY-MM-DD')
  }

  return dateValue.format('YYYY-MM-DD')
}
