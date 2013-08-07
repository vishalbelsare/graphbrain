package com.graphbrain.db


case class ContextNode(store: VertexStore, userId: String, name: String, access: String="public", summary: String="") extends Textual {
  
  override val id = userId + "/context/" + ID.sanitize(name).toLowerCase

  override def extendedId: String = userId + "/context/" + ID.sanitize(name)

  override def put(): Vertex = {
    val template = store.backend.tpUserSpace
    val updater = template.createUpdater(id)
    updater.setString("name", name)
    updater.setString("access", access)
    if ((summary != "") && (summary != null))
      updater.setString("summary", summary)
    template.update(updater)
    store.onPut(this)
    this
  }

  override def clone(newid: String) = ContextNode(store, userId, name, access, summary)

  override def toString: String = name

  override def updateSummary: Textual = ContextNode(store, userId, name, access, generateSummary)

  override def raw: String = {
    "type: " + "context<br />" +
    "userId: " + userId + "<br />" +
    "name: " + name + "<br />" +
    "access: " + access + "<br />" +
    "summary: " + summary + "<br />"
  }
}


object ContextNode {
  def fromId(store: VertexStore, contextId: String, access: String): ContextNode = {
    val userId = ID.ownerId(contextId)
    val name = ID.humanReadable(contextId)
    ContextNode(store, userId, name, access)
  }
}