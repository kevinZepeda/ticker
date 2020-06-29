import {
  IUserProfile,
  IUserTicket,
  IDevices,
  } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setTickets(state: AdminState, payload: IUserTicket[]) {
        state.tickets = payload;
    },
    // setDevices(state: AdminState, payload: IDevices[]) {
    //     state.devices = payload;
    // },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setTicket(state: AdminState, payload: IUserTicket) {
        const tickets = state.tickets.filter((user: IUserTicket) => tickets.id !== payload.id);
        tickets.push(payload);
        state.tickets = tickets;
    },
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetTicket = commit(mutations.setTicket);
export const commitSetUsers = commit(mutations.setUsers);
export const commitSetTickets = commit(mutations.setTickets);
// export const commitSetDevices = commit(mutations.setDevices);
