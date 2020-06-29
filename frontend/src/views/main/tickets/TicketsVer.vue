<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Tickets
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/tickets/create">Create Ticket</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="tickets">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.title }}</td>
        <td>{{ props.item.description }}</td>
        <td>{{ props.item.devices }}</td>
        <td><v-icon v-if="props.item.is_active">checkmark</v-icon></td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-tickets-update', params: {id: props.item.id}}" :disabled="props.item.is_active">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
          <v-btn @click="print(props.item.devices, params={description: props.item.description, tenant: props.item.tenant, vrf: props.item.vrf, category1: props.item.category1, category2: props.item.category2, category3: props.item.category3})">Active</v-btn>
          <v-tooltip top>
            <span>View</span>
            <v-btn slot="activator" flat :to="{name: 'main-tickets-view', params: {id: props.item.id}}">
              <v-icon>visibility</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import axios from 'axios';
import { IUserTicket } from '@/interfaces';
import { readAdminTickets } from '@/store/admin/getters';
import { dispatchGetTickets } from '@/store/admin/actions';

@Component
export default class AdminTickets extends Vue {
  public headers = [
    {
      text: 'Titulo',
      sortable: true,
      value: 'title',
      align: 'left',
    },
    {
      text: 'Descripcion',
      sortable: true,
      value: 'description',
      align: 'left',
    },
    {
      text: 'Devices',
      sortable: true,
      value: 'devices',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get tickets() {
    return readAdminTickets(this.$store);
  }

  public print(ips: string, params) {
    const listIps = ips.split('\n');

    for (const i of listIps) {
      // alert(i + '\n' + params.description + '\n' + params.tenant + '\n' + params.vrf + '\n' + params.category1 + '\n' + params.category2 + '\n' + params.category3);
      axios.post('http://netbox.kinetworking.com:32768/api/ipam/ip-addresses/' , {
        address: i,
        status: 'active',
        description: params.description,
        tenant: params.tenant,
        vrf: params.vrf,
        tags: [
          params.category1,
          params.category2,
          params.category3,
        ],
      }, {
        headers: {
          'Authorization': 'Token 0123456789abcdef0123456789abcdef01234567',
          'Content-Type': 'application/json',
          'Accept': 'application/json; indent=4',
        },
      }).then( (response) => {
        console.log(response);
      });
    }
  }

  public async mounted() {
    await dispatchGetTickets(this.$store);
  }

}
</script>
