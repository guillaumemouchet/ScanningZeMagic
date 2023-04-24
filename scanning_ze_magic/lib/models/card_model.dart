import 'dart:convert';

import 'package:flutter/foundation.dart';

class CardItem {
  final String name;
  //final String extension;
  final int cmc;
  final Uint8List image;
  final String creatureType;
  final int power;
  final int toughness;
  final List colors;
  final String isVanilla;

  CardItem({
    required this.name,
    required this.cmc,
    required this.image,
    required this.creatureType,
    required this.power,
    required this.toughness,
    required this.colors,
    required this.isVanilla,
  });

  factory CardItem.fromJson(Map json) {
    return CardItem(
        name: json["name"],
        cmc: json["cmc"],
        image: base64Decode(json["image"]),
        creatureType: json["creature_type"],
        power: int.parse(json["power"].toString()),
        toughness: int.parse(json["toughness"].toString()),
        colors: json["colors"],
        isVanilla: json["isVanilla"]);
  }
}
