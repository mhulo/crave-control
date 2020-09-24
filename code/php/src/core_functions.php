<?php

	function issue_curl_cmd($cmd_url) {

		$cSession = curl_init(); 
		curl_setopt($cSession,CURLOPT_URL,$cmd_url);
		curl_setopt($cSession,CURLOPT_RETURNTRANSFER,true);
		curl_setopt($cSession,CURLOPT_HEADER, false); 
		$curl_result=curl_exec($cSession);
		curl_close($cSession);
		return $curl_result;
	}

    // unmask incoming framed message
    function websocket_message_unmask($text) {

        $length = ord($text[1]) & 127;
        if($length == 126) {
            $masks = substr($text, 4, 4);
            $data = substr($text, 8);
        }
        elseif($length == 127) {
            $masks = substr($text, 10, 4);
            $data = substr($text, 14);
        }
        else {
            $masks = substr($text, 2, 4);
            $data = substr($text, 6);
        }
        $text = "";
        for ($i = 0; $i < strlen($data); ++$i) {
            $text .= $data[$i] ^ $masks[$i%4];
        }
        return $text;
    }

    // encode message for transfer to client.
    function websocket_message_mask($text) {

        $b1 = 0x80 | (0x1 & 0x0f);
        $length = strlen($text);
        
        if($length <= 125)
            $header = pack('CC', $b1, $length);
        elseif($length > 125 && $length < 65536)
            $header = pack('CCn', $b1, 126, $length);
        elseif($length >= 65536)
            $header = pack('CCNN', $b1, 127, $length);
        return $header.$text;
    }

    // handshake with new client.
    function perform_ws_handshake($receved_header, $client_conn, $host, $port) {

        $headers = array();
        $lines = preg_split("/\r\n/", $receved_header);
        foreach($lines as $line)
        {
            $line = chop($line);
            if(preg_match('/\A(\S+): (.*)\z/', $line, $matches))
            {
                $headers[$matches[1]] = $matches[2];
            }
        }

        $secKey = $headers['Sec-WebSocket-Key'];
        $secAccept = base64_encode(pack('H*', sha1($secKey . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')));
        //handshake header
        $upgrade  = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" .
        "Upgrade: websocket\r\n" .
        "Connection: Upgrade\r\n" .
        "WebSocket-Origin: $host\r\n" .
        "WebSocket-Location: ws://$host:$port/crave/index.php\r\n".
        "Sec-WebSocket-Accept:$secAccept\r\n\r\n";
        socket_write($client_conn,$upgrade,strlen($upgrade));
    }
?>
