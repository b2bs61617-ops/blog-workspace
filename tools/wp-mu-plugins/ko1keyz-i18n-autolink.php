<?php
/**
 * Plugin Name: KO1KEYZ i18n Auto-Link
 * Description: -kr / -en スラッグ命名規則にもとづき、JP / KR / EN の記事を Polylang の翻訳グループへ自動で紐付ける。記事を保存・公開するたびに動作する。
 * Version:     1.0.0
 * Author:      blog-workspace (松)
 *
 * 【なぜ必要か】
 *   Polylang 3.8.7 free の環境では、WP REST API（wp/v2/posts）で `translations` フィールドを
 *   送っても翻訳グループが保存されない（動作検証済み・2026-09-09）。そのため blog-upload
 *   スキルの STEP6/STEP7 で韓国語版・英語版を作っても hreflang が出ない状態になっていた。
 *   このプラグインが save 時に pll_save_post_translations() を代わりに呼んで紐付けを保証する。
 *
 * 【前提となる命名規則】（blog-upload STEP6/7 で必ず守る）
 *   日本語:  {slug}
 *   韓国語:  {slug}-kr      （Polylang 言語 = ko）
 *   英語:    {slug}-en      （Polylang 言語 = en）
 *   ※ Polylang 側の言語割り当て自体は既存フロー（REST の `lang` 指定 など）で行われている前提。
 *     言語が未設定の記事にはこのプラグインは触らない（誤爆防止）。
 *
 * 【インストール】
 *   chomoand-1.com の wp-content/mu-plugins/ に置くだけ（mu-plugins は自動有効・有効化操作不要）。
 *   ディレクトリが無ければ作成する。
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_after_insert_post', 'ko1keyz_i18n_autolink', 20, 2 );

/**
 * 記事保存後に、命名規則から翻訳グループを組み立てて Polylang に保存する。
 *
 * @param int          $post_id
 * @param WP_Post|null  $post
 */
function ko1keyz_i18n_autolink( $post_id, $post = null ) {
	static $running = false;
	if ( $running ) {
		return;
	}

	if ( ! function_exists( 'pll_save_post_translations' ) || ! function_exists( 'pll_get_post_language' ) ) {
		return;
	}

	$post = $post ? $post : get_post( $post_id );
	if ( ! $post || 'post' !== $post->post_type ) {
		return;
	}
	if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) ) {
		return;
	}
	if ( in_array( $post->post_status, array( 'auto-draft', 'trash', 'inherit' ), true ) ) {
		return;
	}

	$slug = $post->post_name;
	if ( '' === $slug ) {
		return;
	}

	// 言語は Polylang の割り当てを信頼する（スラッグからは推測しない＝誤爆防止）。
	$lang = pll_get_post_language( $post_id );
	if ( ! $lang ) {
		return;
	}

	// 実際の言語に応じて、共通のベーススラッグを求める。
	if ( 'ko' === $lang ) {
		$base = preg_replace( '/-kr(-\d+)?$/', '', $slug );
	} elseif ( 'en' === $lang ) {
		$base = preg_replace( '/-en(-\d+)?$/', '', $slug );
	} elseif ( 'ja' === $lang ) {
		$base = $slug;
	} else {
		return; // zh など対象外。
	}
	if ( '' === $base ) {
		return;
	}

	// グループの各メンバーを集める。
	$group = array();

	$group['ja'] = ( 'ja' === $lang ) ? (int) $post_id : ko1keyz_i18n_find( $base, 'ja' );
	$group['ko'] = ( 'ko' === $lang ) ? (int) $post_id : ko1keyz_i18n_find( $base . '-kr', 'ko' );
	$group['en'] = ( 'en' === $lang ) ? (int) $post_id : ko1keyz_i18n_find( $base . '-en', 'en' );

	$group = array_filter( $group ); // 見つからなかった言語を除去。
	if ( count( $group ) < 2 ) {
		return;
	}

	// すでに正しく紐付いていれば何もしない。
	$existing = pll_get_post_translations( $post_id );
	$merged   = $existing;
	foreach ( $group as $l => $pid ) {
		$merged[ $l ] = (int) $pid;
	}
	ksort( $existing );
	ksort( $merged );
	if ( $existing === $merged ) {
		return;
	}

	$running = true;
	pll_save_post_translations( $merged );
	$running = false;
}

/**
 * 指定スラッグ・指定言語の記事 ID を返す（下書き・予約投稿含む）。無ければ 0。
 *
 * @param string $name  post_name（スラッグ）完全一致。
 * @param string $lang  Polylang 言語スラッグ。
 * @return int
 */
function ko1keyz_i18n_find( $name, $lang ) {
	$q = new WP_Query(
		array(
			'post_type'        => 'post',
			'post_status'      => array( 'publish', 'draft', 'pending', 'future', 'private' ),
			'name'             => $name,
			'posts_per_page'   => 1,
			'no_found_rows'    => true,
			'ignore_sticky_posts' => true,
			'lang'             => $lang,
			'suppress_filters' => false,
			'fields'           => 'ids',
		)
	);

	return ! empty( $q->posts ) ? (int) $q->posts[0] : 0;
}
