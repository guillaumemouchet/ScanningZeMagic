import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

import '../models/card_model.dart';

class CardItemDisplay extends StatelessWidget {
  final CardItem card;

  const CardItemDisplay({super.key, required this.card});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4.0,
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: <Widget>[
            Container(
                width: MediaQuery.of(context).size.width * 0.7,
                height: MediaQuery.of(context).size.width * 0.65,
                child: Image.asset("assets/img/${card.image}")),
            //SvgPicture.asset(card.image, semanticsLabel: 'card image')),
            const SizedBox(height: 5),
            Text(
              card.name,
              style: TextStyle(
                  color: Colors.pinkAccent,
                  fontSize: 22,
                  fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 5),
            Text(card.creatureType),
            const SizedBox(height: 5),
            Text(
              card.extension,
              style: TextStyle(color: Colors.black),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 5),
            card.colors.isNotEmpty
                ? Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: card.colors
                        .map(
                          (color) => SvgPicture.asset(
                            'assets/img/$color.svg',
                            // adjust the width as per your requirements
                          ),
                        )
                        .toList(),
                  )
                : Container(),
            const SizedBox(height: 5),
            Text('${card.power}/${card.defense}'),
          ],
        ),
      ),
    );
  }
}
