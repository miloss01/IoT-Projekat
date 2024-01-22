import { Component, OnInit } from '@angular/core';
import { SocketService } from './socket.service';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private socketService: SocketService, private socket: Socket) { }

  persons: number = 0

  dl_value: string = ""
  dpir1_value: number = 0
  dus1_value: number = 0

  ngOnInit(): void {
    this.socketService.getMessage().subscribe(message => {
      console.log(message)
    })

    this.socketService.get_persons().subscribe(message => {
      console.log(message)
      this.persons = message["value"]
    })

    this.socketService.get_DL().subscribe(message => {
      console.log(message)
      this.dl_value = message["value"]
    })

    this.socketService.get_DPIR1().subscribe(message => {
      console.log(message)
      this.dpir1_value = message["value"]
    })

    this.socketService.get_DUS1().subscribe(message => {
      console.log(message)
      this.dus1_value = message["value"]
    })
  }

  probaNaServer() {
    this.socket.emit("probaNaServer", {"naserver": 123})
  }

}
