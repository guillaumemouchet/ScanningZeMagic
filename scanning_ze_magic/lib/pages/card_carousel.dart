import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:scanning_ze_magic/models/card_model.dart';
import 'package:scanning_ze_magic/pages/card_item.dart';
import 'package:stacked_card_carousel/stacked_card_carousel.dart';
import 'package:dio/dio.dart';

//https://www.geeksforgeeks.org/flutter-futurebuilder-widget/
//https://github.com/flutter-devs/flutter_stacked_card_carousel_demo/blob/master/lib/stacked_card_demo.dart
class CardCarousel extends StatefulWidget {
  final Response response;

  const CardCarousel({Key? key, required this.response}) : super(key: key);

  @override
  CardCarouselState createState() => CardCarouselState();
}

class CardCarouselState extends State<CardCarousel> {
  final List<CardItemDisplay> _cardItems = [];
  bool _isLoading = true;

  Future<void> readCards() async {
    final cardData = await json.decode(widget.response.data);
    if (_cardItems.isEmpty) {
      for (final cardItem in cardData) {
        _cardItems.add(CardItemDisplay(card: CardItem.fromJson(cardItem)));
      }
    }
    setState(() {
      _isLoading = false;
    });
  }

  @override
  void initState() {
    super.initState();
    init();
  }

  Future<void> init() async {
    if (_isLoading) {
      await readCards();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Card result')),
      body: FutureBuilder(
        future: init(),
        builder: (BuildContext context, AsyncSnapshot<void> snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return StackedCardCarousel(
              initialOffset: 40,
              spaceBetweenItems: 400,
              items: _cardItems,
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
