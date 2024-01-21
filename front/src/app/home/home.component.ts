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

  ngOnInit(): void {
    this.socketService.getMessage().subscribe(message => {
      console.log(message)
    })
  }

  probaNaServer() {
    this.socket.emit("probaNaServer", {"naserver": 123})
  }

}
