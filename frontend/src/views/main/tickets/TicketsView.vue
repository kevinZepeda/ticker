<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Ticket</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Title</div>
            <div class="title primary--text text--darken-2" v-if="title">{{ticket.title}}</div>
          </div>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Description</div>
            <div class="title primary--text text--darken-2" v-if="description">{{ticket.description}}</div>
          </div>
          <table>
            <tr>
              <th><v-text-field label="Ticket Type" v-model="ticketType" disabled></v-text-field></th>
              <th><v-text-field label="External ID" v-model="externalId" disabled></v-text-field></th>
              <th><v-text-field label="Tenant" v-model="tenant" disabled></v-text-field></th>
            </tr>
            <tr>
              <th><v-text-field label="Region" v-model="region" disabled></v-text-field></th>
              <th><v-text-field label="Request Type" v-model="requestType" disabled></v-text-field></th>
              <th><v-text-field label="VLAN" v-model="vlan" disabled></v-text-field></th>
              <th><v-text-field label="VRF" v-model="vrf" disabled></v-text-field></th>
            </tr>
            <tr>
              <th><v-text-field label="Category 1" v-model="category1" disabled></v-text-field></th>
              <th><v-text-field label="Category 2" v-model="category2" disabled></v-text-field></th>
              <th><v-text-field label="Category 3" v-model="category3" disabled></v-text-field></th>
            </tr>
          </table>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Devices</div>
            <v-data-table :headers="headers" :items="devices">
              <template slot="items" slot-scope="props">
                <td>{{ parseInt(props.item.no) + 1 }}</td>
                <td>{{ props.item.ip }}</td>
                <td>{{ description }}</td>
                <td>{{ region }}</td>
              </template>
            </v-data-table>
          </div>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Status</div>
            <v-checkbox
              label=""
              v-model="isActive"
            ></v-checkbox>
          </div>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="back">Back</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserTicket, IUserTicketUpdate } from '@/interfaces';
import { dispatchGetTickets, dispatchUpdateTicket } from '@/store/admin/actions';
import { readAdminOneTicket } from '@/store/admin/getters';

@Component
export default class EditTicket extends Vue {
  public valid = true;
  public title: string = '';
  public description: string = '';
  public devices;
  public ticketType: string = '';
  public externalId: number = 0;
  public tenant: string = '';
  public region: string = '';
  public requestType: string = '';
  public category1: string = '';
  public category2: string = '';
  public category3: string = '';
  public vlan: string = '';
  public vrf: string = '';
  public isActive: number = 0;
  public headers = [
    {
      text: 'No',
      sortable: true,
      value: 'no',
      align: 'left',
    },
    {
      text: 'IP',
      sortable: true,
      value: 'ip',
      align: 'left',
    },
    {
      text: 'Description',
      sortable: true,
      value: 'description',
      align: 'left',
    },
    {
      text: 'Region',
      sortable: true,
      value: 'region',
      align: 'left',
    },
  ];


  public async mounted() {
    await dispatchGetTickets(this.$store);
    this.reset();
  }

  public reset() {
    this.$validator.reset();
    let ips = {};
    if (this.ticket) {
      this.title = this.ticket.title;
      this.description = this.ticket.description;
      ips = Object.assign({}, this.ticket.devices.split('\n'));
      this.devices = Object.keys(ips).map( (key) => {
        return {no: key, ip: ips[key]};
      });
      this.isActive = this.ticket.is_active;
      this.ticketType = this.ticket.ticketType;
      this.externalId = this.ticket.externalId;
      this.tenant = this.ticket.tenant;
      this.region = this.ticket.region;
      this.requestType = this.ticket.requestType;
      this.category1 = this.ticket.category1;
      this.category2 = this.ticket.category2;
      this.category3 = this.ticket.category3;
      this.vlan = this.ticket.vlan;
      this.vrf = this.ticket.vrf;
    }
  }

  public back() {
    this.$router.back();
  }

  get ticket() {
    return readAdminOneTicket(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
