package com.graphbrain.eco

import scala.collection.mutable

class Contexts(s: String) {
  val ctxts = mutable.ListBuffer[Context]()
  val sentence = parseSentence(s)

  private val addCtxts = mutable.ListBuffer[Context]()
  private val remCtxts = mutable.ListBuffer[Context]()

  def addContext(c: Context) = addCtxts += c
  def remContext(c: Context) = remCtxts += c

  def applyChanges() = {
    for (c <- addCtxts) ctxts += c
    for (c <- remCtxts) ctxts -= c
    addCtxts.clear()
    remCtxts.clear()
  }

  private def parseSentence(s: String) = s.split(" ")

  def print() = {
    for (c <- ctxts) c.print()
  }
}