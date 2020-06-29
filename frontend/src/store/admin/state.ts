import { IUserProfile, IUserTicket, IDevices } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    tickets: IUserTicket[];
    // devices: IDevices[];
}
