import 'package:flutter/material.dart';

class CardItem {
  final String name;
  final String extension;
  final String image;
  final String creatureType;
  final int power;
  final int defense;
  final List colors;

  CardItem({
    required this.name,
    required this.extension,
    required this.image,
    required this.creatureType,
    required this.power,
    required this.defense,
    required this.colors,
  });

  factory CardItem.fromJson(Map json) {
    return CardItem(
        name: json["name"],
        extension: json["extension"],
        image: json["image"],
        creatureType: json["creature_type"],
        power: int.parse(json["power"].toString()),
        defense: int.parse(json["defense"].toString()),
        colors: json["colors"]);
  }
}
