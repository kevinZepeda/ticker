export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserTicket {
  id: number;
  title: string;
  description: string;
  devices: string;
  is_active: number;
  ticketType: string;
  externalId: number;
  tenant: string;
  region: string;
  requestType: string;
  category1: string;
  category2: string;
  category3: string;
  vlan: string;
  vrf: string;
}

export interface IUserTicketUpdate {
  title?: string;
  description?: string;
  devices?: string;
  is_active?: number;
  ticketType?: string;
  externalId?: number;
  tenant?: string;
  region?: string;
  requestType?: string;
  category1?: string;
  category2?: string;
  category3?: string;
  vlan?: string;
  vrf?: string;
}

export interface IUserTicketCreate {
  title?: string;
  description?: string;
  devices?: string;
  is_active?: number;
  ticketType?: string;
  externalId?: number;
  tenant?: string;
  region?: string;
  requestType?: string;
  category1?: string;
  category2?: string;
  category3?: string;
  vlan?: string;
  vrf?: string;
}

export interface IDevices {
    count: number;
    next: string;
    previous: string;
    results: string;
}
