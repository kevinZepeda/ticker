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
            <div
              class="title primary--text text--darken-2"
              v-if="title"
            >{{ticket.title}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Description"
              v-model="description"
              disabled
            ></v-text-field>
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
            <v-textarea
              outlined
              v-model="devices"
              label="IP's separated by enter"
              disabled
            ></v-textarea>
            <div class="subheading secondary--text text--lighten-2">Ticket is active <span v-if="isActive">(currently active)</span><span v-else>(currently not active)</span></div>
            <v-checkbox
              label="Is Active"
              v-model="isActive"
            ></v-checkbox>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn@click="submit">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserTicket, IUserTicketUpdate } from '@/interfaces';
import axios from 'axios';
import { dispatchGetTickets, dispatchUpdateTicket } from '@/store/admin/actions';
import { readAdminOneTicket } from '@/store/admin/getters';

@Component
export default class EditTicket extends Vue {
  public valid = true;
  public title: string = '';
  public description: string = '';
  public devices: string = '';
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


  public async mounted() {
    await dispatchGetTickets(this.$store);
    this.reset();
  }

  public reset() {
    this.$validator.reset();
    if (this.ticket) {
      this.title = this.ticket.title;
      this.description = this.ticket.description;
      this.devices = this.ticket.devices;
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

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    const listIps = this.devices.split('\n');

    if (this.isActive) {
      for (const i of listIps) {
        axios.post('http://netbox.kinetworking.com:32768/api/ipam/ip-addresses/' , {
          address: i,
          status: 'active',
          description: this.description,
          tenant: this.tenant,
          vrf: this.vrf,
          tags: [
            this.category1,
            this.category2,
            this.category3,
          ],
        }, {
          headers: {
            'Authorization': 'Token 0123456789abcdef0123456789abcdef01234567',
            'Content-Type': 'application/json',
            'Accept': 'application/json; indent=4',
          },
        }).then( (response) => {
          alert(response);
        });
      }
    }
    if (await this.$validator.validateAll()) {
      const updatedTicket: IUserTicketUpdate = {};
      if (this.title) {
        updatedTicket.title = this.title;
      }
      if (this.description) {
        updatedTicket.description = this.description;
      }
      if (this.devices) {
        updatedTicket.devices = this.devices;
      }
      updatedTicket.is_active = this.isActive;
      await dispatchUpdateTicket(this.$store, { id: this.ticket!.id, ticket: updatedTicket });
      this.$router.push('/main/tickets');
    }
  }

  get ticket() {
    return readAdminOneTicket(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
