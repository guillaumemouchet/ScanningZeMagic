import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:scanning_ze_magic/models/card_model.dart';
import 'package:scanning_ze_magic/pages/CardItem.dart';
import 'package:stacked_card_carousel/stacked_card_carousel.dart';

class CardCarousel extends StatefulWidget {
  const CardCarousel({super.key});
  @override
  CardCarouselState createState() => CardCarouselState();
}

class CardCarouselState extends State<CardCarousel> {
  //final List<CardItem> _cards = [];
  final List<CardItemDisplay> _cardItems = [];

  Future<void> readCards() async {
    final String cardResponse =
        await rootBundle.loadString('assets/data/card_data.json');
    final cardData = await json.decode(cardResponse);
    for (final cardItem in cardData) {
      _cardItems.add(CardItemDisplay(card: CardItem.fromJson(cardItem)));
    }
    setState(() {});
  }

  Future<void> init() async {
    await readCards();
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Card result')),
        body: FutureBuilder(
          builder: (context, snapshot) {
            if (_cardItems.isNotEmpty) {
              return StackedCardCarousel(
                initialOffset: 40,
                spaceBetweenItems: 400,
                items: _cardItems,
              );
            }
            return Center(
              child: CircularProgressIndicator(),
            );
          },
          future: init(),
        ));
  }
}
