package com.graphbrain.db

abstract class Vertex(val id: String, val degree: Int = 0, val ts: Long = -1) {

  def this(id: String, map: Map[String, String]) =
    this(id, map("degree").toInt, map("ts").toLong)

  def extraMap: Map[String, String]

  def toMap: Map[String, String] =
    Map("degree" -> degree.toString,
      "ts" -> ts.toString) ++
    extraMap

  def setId(newId: String): Vertex

  def setDegree(newDegree: Int): Vertex

  def setTs(newTs: Long): Vertex

  def toGlobal: Vertex = setId(ID.userToGlobal(id))

  def toUser(userId: String): Vertex = setId(ID.globalToUser(id, userId))

  override def toString: String = id

  def description: String = toString

  def raw: String = ""

  def shouldUpdate(graph: Graph): Boolean = !graph.exists(id)

  def updateFromEdges(): Vertex = this

  override def equals(o: Any) = o match {
    case that: Vertex => that.id == id
    case _ => false
  }

  override def hashCode = id.hashCode
}

object Vertex {
  def cleanId(id: String) = id.toLowerCase
}