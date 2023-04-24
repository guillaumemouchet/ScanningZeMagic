import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:io';

import 'package:scanning_ze_magic/pages/card_carousel.dart';

class CameraDisplay extends StatefulWidget {
  const CameraDisplay({super.key, required this.camera});
  final CameraDescription camera;
  @override
  CameraDisplayState createState() => CameraDisplayState();
}

class CameraDisplayState extends State<CameraDisplay> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    // create a CameraController.
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.camera,
      // Define the resolution to use.
      ResolutionPreset.medium,
    );

    // Next, initialize the controller. This returns a Future.
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Take a picture')),
      // You must wait until the controller is initialized before displaying the
      // camera preview. Use a FutureBuilder to display a loading spinner until the
      // controller has finished initializing.
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // If the Future is complete, display the preview.
            return CameraPreview(_controller);
          } else {
            // Otherwise, display a loading indicator.
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        // Provide an onPressed callback.
        onPressed: () async {
          // Take the Picture in a try / catch block. If anything goes wrong,
          // catch the error.
          try {
            // Ensure that the camera is initialized.
            await _initializeControllerFuture;

            // Attempt to take a picture and get the file `image`
            // where it was saved.
            final image = await _controller.takePicture();

            if (!mounted) return;

            // If the picture was taken, display it on a new screen.
            await Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => DisplayPictureScreen(
                  // Pass the automatically generated path to
                  // the DisplayPictureScreen widget.
                  imagePath: image.path,
                ),
              ),
            );
          } catch (e) {
            // If an error occurs, log the error to the console.
            print(e);
          }
        },
        child: const Icon(Icons.camera_alt),
      ),
    );
  }
}

// A widget that displays the picture taken by the user.
class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;
  const DisplayPictureScreen({super.key, required this.imagePath});

  //https://stackoverflow.com/questions/44841729/how-to-upload-images-to-server-in-flutter/49645074#49645074
  Future<Response<String>> uploadImage(File file) async {
    String fileName = file.path.split('/').last;
    print(file.path);
    final Dio dio = Dio();
    FormData formData = FormData.fromMap({
      "file": await MultipartFile.fromFile(file.path, filename: fileName),
    });
    Response<String> response =
        await dio.post("http://10.0.2.2:5000/uploadImage", data: formData);
    return response;
  }

  Future<Response<String>> sendAssetImage() async {
    ByteData assetData = await rootBundle.load("assets/img/mtg_phone.jpg");
    List<int> bytes = assetData.buffer.asUint8List();
    FormData formData = FormData.fromMap(
        {'file': MultipartFile.fromBytes(bytes, filename: 'mtg_phone.jpg')});

    final Dio dio = Dio();

    dio.options.receiveTimeout = Duration(seconds: 60);

    Response<String> response =
        await dio.post("http://10.0.2.2:5000/uploadImage", data: formData);
    print('Response status: ${response.statusCode}');
    print('Response data: ${response.data}');

    return response;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Display the Picture')),
        // The image is stored as a file on the device. Use the `Image.file`
        // constructor with the given path to display the image.
        body: Center(
          child: Column(children: [
            ElevatedButton(
                onPressed: () async {
                  print("sending");
                  try {
                    //final response = await uploadImage(File(imagePath));
                    final response = await sendAssetImage();
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => CardCarousel(
                                  response: response,
                                )));
                  } on Error catch (e) {
                    print(e);
                  }
                },
                child: const Text("Submit this picture")),
            Image.file(File(imagePath)),
          ]),
        ));
  }
}
