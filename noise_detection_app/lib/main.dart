import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:noise_detection_app/services/web_service.dart';
import 'package:web_socket_channel/io.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final WebService _webService = WebService();
  IOWebSocketChannel _channel;

  @override
  Widget build(BuildContext context) {
    _webService.main();

    return Scaffold(
      appBar: AppBar(
        title: Text('Noise Level Detection'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // StreamBuilder(
            //   builder: (context, snapshot) {
            //
            //     if (snapshot.hasError) {
            //       return Text(snapshot.error.toString());
            //     }
            //
            //     if (snapshot.hasData) {
            //       return Text(snapshot.data);
            //     }
            //
            //     _channel.sink.add('pls work');
            //     return CircularProgressIndicator();
            //   },
            // ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    // _channel.sink.close();
    super.dispose();
  }
}