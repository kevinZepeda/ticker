import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    adminUsers: (state: AdminState) => state.users,
    adminTickets: (state: AdminState) => state.tickets,
    adminOneUser: (state: AdminState) => (userId: number) => {
        const filteredUsers = state.users.filter((user) => user.id === userId);
        if (filteredUsers.length > 0) {
            return { ...filteredUsers[0] };
        }
    },
    adminOneTicket: (state: AdminState) => (ticketId: number) => {
        const filteredTickets = state.tickets.filter((ticket) => ticket.id === ticketId);
        if (filteredTickets.length > 0) {
            return { ...filteredTickets[0] };
        }
    },
};

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminOneTicket = read(getters.adminOneTicket);
export const readAdminUsers = read(getters.adminUsers);
export const readAdminTickets = read(getters.adminTickets);
